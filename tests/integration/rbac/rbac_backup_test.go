// Licensed to the LF AI & Data foundation under one
// or more contributor license agreements. See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership. The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License. You may obtain a copy of the License at
//
//	http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
package rbac

import (
	"context"
	"fmt"
	"math/rand"
	"strings"

	"github.com/samber/lo"
	"google.golang.org/grpc/metadata"

	"github.com/milvus-io/milvus-proto/go-api/v2/commonpb"
	"github.com/milvus-io/milvus-proto/go-api/v2/milvuspb"
	"github.com/milvus-io/milvus/pkg/v2/util"
	"github.com/milvus-io/milvus/pkg/v2/util/crypto"
	"github.com/milvus-io/milvus/pkg/v2/util/merr"
)

const (
	dim            = 128
	dbName         = ""
	collectionName = "test_load_collection"
)

func GetContext(ctx context.Context, originValue string) context.Context {
	authKey := strings.ToLower(util.HeaderAuthorize)
	authValue := crypto.Base64Encode(originValue)
	contextMap := map[string]string{
		authKey: authValue,
	}
	md := metadata.New(contextMap)
	return metadata.NewOutgoingContext(ctx, md)
}

func (s *RBACBasicTestSuite) TestBackup() {
	ctx := GetContext(context.Background(), defaultAuth)

	createRole := func(name string) {
		resp, err := s.Cluster.MilvusClient.CreateRole(ctx, &milvuspb.CreateRoleRequest{
			Entity: &milvuspb.RoleEntity{Name: name},
		})
		s.NoError(err)
		s.True(merr.Ok(resp))
	}

	operatePrivilege := func(role, privilege, objectName, dbName string, operateType milvuspb.OperatePrivilegeType) {
		resp, err := s.Cluster.MilvusClient.OperatePrivilege(ctx, &milvuspb.OperatePrivilegeRequest{
			Type: operateType,
			Entity: &milvuspb.GrantEntity{
				Role:       &milvuspb.RoleEntity{Name: role},
				Object:     &milvuspb.ObjectEntity{Name: commonpb.ObjectType_Global.String()},
				ObjectName: collectionName,
				DbName:     dbName,
				Grantor: &milvuspb.GrantorEntity{
					User:      &milvuspb.UserEntity{Name: util.UserRoot},
					Privilege: &milvuspb.PrivilegeEntity{Name: privilege},
				},
			},
			Version: "v2",
		})
		s.NoError(err)
		s.True(merr.Ok(resp))
	}

	// test empty rbac content
	emptyBackupRBACResp, err := s.Cluster.MilvusClient.BackupRBAC(ctx, &milvuspb.BackupRBACMetaRequest{})
	s.NoError(err)
	s.True(merr.Ok(emptyBackupRBACResp.GetStatus()))
	s.Equal("", emptyBackupRBACResp.GetRBACMeta().String())

	// generate some rbac content
	// create role test_role
	roleName := fmt.Sprintf("test_role_%d", rand.Int31n(1000000))
	createRole(roleName)

	// grant collection level search privilege to role test_role
	operatePrivilege(roleName, "Search", util.AnyWord, util.DefaultDBName, milvuspb.OperatePrivilegeType_Grant)

	// create privilege group test_group
	groupName := fmt.Sprintf("test_group_%d", rand.Int31n(1000000))
	createPrivGroupResp, err := s.Cluster.MilvusClient.CreatePrivilegeGroup(ctx, &milvuspb.CreatePrivilegeGroupRequest{
		GroupName: groupName,
	})
	s.NoError(err)
	s.True(merr.Ok(createPrivGroupResp))

	collectionPrivileges := []*milvuspb.PrivilegeEntity{{Name: "Query"}, {Name: "Insert"}}
	for _, p := range collectionPrivileges {
		s.Equal(milvuspb.PrivilegeLevel_Collection.String(), util.GetPrivilegeLevel(p.Name))
	}

	// add query and insert privilege to group test_group
	addPrivsToGroupResp, err := s.Cluster.MilvusClient.OperatePrivilegeGroup(ctx, &milvuspb.OperatePrivilegeGroupRequest{
		GroupName:  groupName,
		Privileges: []*milvuspb.PrivilegeEntity{{Name: "Query"}, {Name: "Insert"}},
		Type:       milvuspb.OperatePrivilegeGroupType_AddPrivilegesToGroup,
	})
	s.NoError(err)
	s.True(merr.Ok(addPrivsToGroupResp))

	// grant privilege group test_group to role test_role
	operatePrivilege(roleName, groupName, util.AnyWord, util.DefaultDBName, milvuspb.OperatePrivilegeType_Grant)

	userName := "test_user"
	passwd := "test_passwd"
	createCredResp, err := s.Cluster.MilvusClient.CreateCredential(ctx, &milvuspb.CreateCredentialRequest{
		Username: userName,
		Password: crypto.Base64Encode(passwd),
	})
	s.NoError(err)
	s.True(merr.Ok(createCredResp))
	operateUserRoleResp, err := s.Cluster.MilvusClient.OperateUserRole(ctx, &milvuspb.OperateUserRoleRequest{
		Username: userName,
		RoleName: roleName,
	})
	s.NoError(err)
	s.True(merr.Ok(operateUserRoleResp))

	// test back up rbac, grants should contain
	backupRBACResp, err := s.Cluster.MilvusClient.BackupRBAC(ctx, &milvuspb.BackupRBACMetaRequest{})
	s.NoError(err)
	s.True(merr.Ok(backupRBACResp.GetStatus()))
	s.Equal(2, len(backupRBACResp.GetRBACMeta().Grants))
	grants := lo.SliceToMap(backupRBACResp.GetRBACMeta().Grants, func(g *milvuspb.GrantEntity) (string, *milvuspb.GrantEntity) {
		return g.Grantor.Privilege.Name, g
	})
	s.True(grants["Search"] != nil)
	s.True(grants[groupName] != nil)
	s.Equal(groupName, backupRBACResp.GetRBACMeta().PrivilegeGroups[0].GroupName)
	s.Equal(2, len(backupRBACResp.GetRBACMeta().PrivilegeGroups[0].Privileges))

	restoreRBACResp, err := s.Cluster.MilvusClient.RestoreRBAC(ctx, &milvuspb.RestoreRBACMetaRequest{})
	s.NoError(err)
	s.True(merr.Ok(restoreRBACResp))

	// test restore, expect to failed due to role/user already exist
	restoreRBACResp, err = s.Cluster.MilvusClient.RestoreRBAC(ctx, &milvuspb.RestoreRBACMetaRequest{
		RBACMeta: backupRBACResp.GetRBACMeta(),
	})
	s.NoError(err)
	s.False(merr.Ok(restoreRBACResp))

	// revoke privilege search from role test_role before dropping the role
	operatePrivilege(roleName, "Search", util.AnyWord, util.DefaultDBName, milvuspb.OperatePrivilegeType_Revoke)

	// revoke privilege group test_group from role test_role before dropping the role
	operatePrivilege(roleName, groupName, util.AnyWord, util.DefaultDBName, milvuspb.OperatePrivilegeType_Revoke)

	// drop privilege group test_group
	dropPrivGroupResp, err := s.Cluster.MilvusClient.DropPrivilegeGroup(ctx, &milvuspb.DropPrivilegeGroupRequest{
		GroupName: groupName,
	})
	s.NoError(err)
	s.True(merr.Ok(dropPrivGroupResp))

	// drop role test_role
	dropRoleResp, err := s.Cluster.MilvusClient.DropRole(ctx, &milvuspb.DropRoleRequest{
		RoleName: roleName,
	})
	s.NoError(err)
	s.True(merr.Ok(dropRoleResp))

	// delete credential
	delCredResp, err := s.Cluster.MilvusClient.DeleteCredential(ctx, &milvuspb.DeleteCredentialRequest{
		Username: userName,
	})
	s.NoError(err)
	s.True(merr.Ok(delCredResp))

	// restore rbac
	restoreRBACResp, err = s.Cluster.MilvusClient.RestoreRBAC(ctx, &milvuspb.RestoreRBACMetaRequest{
		RBACMeta: backupRBACResp.GetRBACMeta(),
	})
	s.NoError(err)
	s.True(merr.Ok(restoreRBACResp))

	// check the restored rbac, should be same as the original one
	backupRBACResp2, err := s.Cluster.MilvusClient.BackupRBAC(ctx, &milvuspb.BackupRBACMetaRequest{})
	s.NoError(err)
	s.True(merr.Ok(backupRBACResp2.GetStatus()))
	s.Equal(backupRBACResp2.GetRBACMeta().String(), backupRBACResp.GetRBACMeta().String())

	// clean rbac meta
	operatePrivilege(roleName, "Search", util.AnyWord, util.DefaultDBName, milvuspb.OperatePrivilegeType_Revoke)

	operatePrivilege(roleName, groupName, util.AnyWord, util.DefaultDBName, milvuspb.OperatePrivilegeType_Revoke)

	dropPrivGroupResp2, err := s.Cluster.MilvusClient.DropPrivilegeGroup(ctx, &milvuspb.DropPrivilegeGroupRequest{
		GroupName: groupName,
	})
	s.NoError(err)
	s.True(merr.Ok(dropPrivGroupResp2))

	dropRoleResp2, err := s.Cluster.MilvusClient.DropRole(ctx, &milvuspb.DropRoleRequest{
		RoleName: roleName,
	})
	s.NoError(err)
	s.True(merr.Ok(dropRoleResp2))

	delCredResp2, err := s.Cluster.MilvusClient.DeleteCredential(ctx, &milvuspb.DeleteCredentialRequest{
		Username: userName,
	})
	s.NoError(err)
	s.True(merr.Ok(delCredResp2))
}
