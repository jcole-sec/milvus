// Licensed to the LF AI & Data foundation under one
// or more contributor license agreements. See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership. The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License. You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package hellomilvus

import (
	"context"
	"fmt"
	"time"

	"github.com/samber/lo"
	"go.uber.org/zap"
	"google.golang.org/protobuf/proto"

	"github.com/milvus-io/milvus-proto/go-api/v2/commonpb"
	"github.com/milvus-io/milvus-proto/go-api/v2/milvuspb"
	"github.com/milvus-io/milvus-proto/go-api/v2/schemapb"
	"github.com/milvus-io/milvus/pkg/v2/common"
	"github.com/milvus-io/milvus/pkg/v2/log"
	"github.com/milvus-io/milvus/pkg/v2/proto/datapb"
	"github.com/milvus-io/milvus/pkg/v2/util/funcutil"
	"github.com/milvus-io/milvus/pkg/v2/util/merr"
	"github.com/milvus-io/milvus/pkg/v2/util/metric"
	"github.com/milvus-io/milvus/tests/integration"
)

func (s *HelloMilvusSuite) TestHelloStreaming() {
	ctx, cancel := context.WithTimeout(context.Background(), time.Minute*10)
	defer cancel()
	c := s.Cluster

	const (
		dim    = 128
		dbName = ""
		rowNum = 100000

		indexType  = integration.IndexFaissIvfFlat
		metricType = metric.L2
		vecType    = schemapb.DataType_FloatVector
	)

	collectionName := "TestHelloStreaming_" + funcutil.GenRandomStr()

	schema := integration.ConstructSchemaOfVecDataType(collectionName, dim, false, vecType)
	marshaledSchema, err := proto.Marshal(schema)
	s.NoError(err)

	// create collection
	createCollectionStatus, err := c.MilvusClient.CreateCollection(ctx, &milvuspb.CreateCollectionRequest{
		DbName:           dbName,
		CollectionName:   collectionName,
		Schema:           marshaledSchema,
		ShardsNum:        common.DefaultShardsNum,
		ConsistencyLevel: commonpb.ConsistencyLevel_Strong,
	})
	err = merr.CheckRPCCall(createCollectionStatus, err)
	s.NoError(err)
	log.Info("CreateCollection result", zap.Any("createCollectionStatus", createCollectionStatus))

	// show collection
	showCollectionsResp, err := c.MilvusClient.ShowCollections(ctx, &milvuspb.ShowCollectionsRequest{})
	err = merr.CheckRPCCall(showCollectionsResp, err)
	s.NoError(err)
	log.Info("ShowCollections result", zap.Any("showCollectionsResp", showCollectionsResp))

	// insert
	pkColumn := integration.NewInt64FieldData(integration.Int64Field, rowNum)
	fVecColumn := integration.NewFloatVectorFieldData(integration.FloatVecField, rowNum, dim)
	hashKeys := integration.GenerateHashKeys(rowNum)
	insertResult, err := c.MilvusClient.Insert(ctx, &milvuspb.InsertRequest{
		DbName:         dbName,
		CollectionName: collectionName,
		FieldsData:     []*schemapb.FieldData{pkColumn, fVecColumn},
		HashKeys:       hashKeys,
		NumRows:        uint32(rowNum),
	})
	err = merr.CheckRPCCall(insertResult, err)
	s.NoError(err)
	s.Equal(int64(rowNum), insertResult.GetInsertCnt())

	// delete
	deleteResult, err := c.MilvusClient.Delete(ctx, &milvuspb.DeleteRequest{
		DbName:         dbName,
		CollectionName: collectionName,
		Expr:           integration.Int64Field + " in [1, 2]",
	})
	err = merr.CheckRPCCall(deleteResult, err)
	s.NoError(err)

	// flush
	flushResp, err := c.MilvusClient.Flush(ctx, &milvuspb.FlushRequest{
		DbName:          dbName,
		CollectionNames: []string{collectionName},
	})
	err = merr.CheckRPCCall(flushResp, err)
	s.NoError(err)
	s.T().Logf("flush response, flushTs=%d, segmentIDs=%v", flushResp.GetCollFlushTs()[collectionName], flushResp.GetCollSegIDs()[collectionName])
	segmentIDs, has := flushResp.GetCollSegIDs()[collectionName]
	ids := segmentIDs.GetData()
	s.Require().NotEmpty(segmentIDs)
	s.Require().True(has)
	flushTs, has := flushResp.GetCollFlushTs()[collectionName]
	s.True(has)
	s.WaitForFlush(ctx, ids, flushTs, dbName, collectionName)

	// create index
	createIndexStatus, err := c.MilvusClient.CreateIndex(ctx, &milvuspb.CreateIndexRequest{
		CollectionName: collectionName,
		FieldName:      integration.FloatVecField,
		IndexName:      "_default",
		ExtraParams:    integration.ConstructIndexParam(dim, indexType, metricType),
	})
	err = merr.CheckRPCCall(createIndexStatus, err)
	s.NoError(err)
	s.WaitForIndexBuilt(ctx, collectionName, integration.FloatVecField)

	segments, err := c.ShowSegments(collectionName)
	s.NoError(err)
	s.NotEmpty(segments)
	flushedSegment := lo.Filter(segments, func(info *datapb.SegmentInfo, i int) bool {
		return info.GetState() == commonpb.SegmentState_Flushed || info.GetState() == commonpb.SegmentState_Flushing
	})
	s.Equal(2, len(flushedSegment))
	s.Equal(int64(rowNum), segments[0].GetNumOfRows())

	// load
	loadStatus, err := c.MilvusClient.LoadCollection(ctx, &milvuspb.LoadCollectionRequest{
		DbName:         dbName,
		CollectionName: collectionName,
	})
	err = merr.CheckRPCCall(loadStatus, err)
	s.NoError(err)
	s.WaitForLoad(ctx, collectionName)

	// search
	expr := fmt.Sprintf("%s > 0", integration.Int64Field)
	nq := 10
	topk := 10
	roundDecimal := -1
	params := integration.GetSearchParams(indexType, metricType)
	searchReq := integration.ConstructSearchRequest("", collectionName, expr,
		integration.FloatVecField, vecType, nil, metricType, params, nq, dim, topk, roundDecimal)

	searchResult, err := c.MilvusClient.Search(ctx, searchReq)
	err = merr.CheckRPCCall(searchResult, err)
	s.NoError(err)
	s.Equal(nq*topk, len(searchResult.GetResults().GetScores()))

	// query
	queryResult, err := c.MilvusClient.Query(ctx, &milvuspb.QueryRequest{
		DbName:         dbName,
		CollectionName: collectionName,
		Expr:           "",
		OutputFields:   []string{"count(*)"},
	})
	err = merr.CheckRPCCall(queryResult, err)
	s.NoError(err)
	s.Equal(int64(rowNum-2), queryResult.GetFieldsData()[0].GetScalars().GetLongData().GetData()[0])

	// release collection
	status, err := c.MilvusClient.ReleaseCollection(ctx, &milvuspb.ReleaseCollectionRequest{
		CollectionName: collectionName,
	})
	err = merr.CheckRPCCall(status, err)
	s.NoError(err)

	// drop collection
	status, err = c.MilvusClient.DropCollection(ctx, &milvuspb.DropCollectionRequest{
		CollectionName: collectionName,
	})
	err = merr.CheckRPCCall(status, err)
	s.NoError(err)
}
