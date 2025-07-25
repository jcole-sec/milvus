import json

from pymilvus import (
    FieldSchema,
    CollectionSchema,
    DataType,
    Function,
    FunctionType,
    AnnSearchRequest,
    WeightedRanker,
)
from common.common_type import CaseLabel, CheckTasks
from common import common_func as cf
from common import common_type as ct
from utils.util_log import test_log as log
from base.client_base import TestcaseBase

import random
import pytest
import pandas as pd
from faker import Faker

Faker.seed(19530)
fake_en = Faker("en_US")
fake_zh = Faker("zh_CN")
fake_jp = Faker("ja_JP")
fake_de = Faker("de_DE")

# patch faker to generate text with specific distribution
cf.patch_faker_text(fake_en, cf.en_vocabularies_distribution)
cf.patch_faker_text(fake_zh, cf.zh_vocabularies_distribution)

pd.set_option("expand_frame_repr", False)

prefix = "full_text_search_collection"


class TestCreateCollectionWIthFullTextSearch(TestcaseBase):
    """
    ******************************************************************
      The following cases are used to test create collection with full text search
    ******************************************************************
    """

    @pytest.mark.tags(CaseLabel.L0)
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_create_collection_for_full_text_search(self, tokenizer):
        """
        target: test create collection with full text search
        method: create collection with full text search, use bm25 function
        expected: create collection successfully
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
            FieldSchema(
                name="paragraph_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR
            ),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        text_fields = ["text", "paragraph"]
        for field in text_fields:
            bm25_function = Function(
                name=f"{field}_bm25_emb",
                function_type=FunctionType.BM25,
                input_field_names=[field],
                output_field_names=[f"{field}_sparse_emb"],
                params={},
            )
            schema.add_function(bm25_function)
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        res, _ = collection_w.describe()
        assert len(res["functions"]) == len(text_fields)

    @pytest.mark.tags(CaseLabel.L0)
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_create_collection_for_full_text_search_twice_with_same_schema(
        self, tokenizer
    ):
        """
        target: test create collection with full text search twice with same schema
        method: create collection with full text search, use bm25 function, then create again
        expected: create collection successfully and create again successfully
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
            FieldSchema(
                name="paragraph_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR
            ),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        text_fields = ["text", "paragraph"]
        for field in text_fields:
            bm25_function = Function(
                name=f"{field}_bm25_emb",
                function_type=FunctionType.BM25,
                input_field_names=[field],
                output_field_names=[f"{field}_sparse_emb"],
                params={},
            )
            schema.add_function(bm25_function)
        c_name = cf.gen_unique_str(prefix)
        self.init_collection_wrap(name=c_name, schema=schema)
        collection_w = self.init_collection_wrap(name=c_name, schema=schema)
        res, _ = collection_w.describe()
        assert len(res["functions"]) == len(text_fields)


# @pytest.mark.skip("skip")
class TestCreateCollectionWithFullTextSearchNegative(TestcaseBase):
    """
    ******************************************************************
      The following cases are used to test create collection with full text search negative
    ******************************************************************
    """

    @pytest.mark.tags(CaseLabel.L1)
    @pytest.mark.parametrize("tokenizer", ["unsupported"])
    @pytest.mark.skip(reason="check not implement may cause panic")
    def test_create_collection_for_full_text_search_with_unsupported_tokenizer(
        self, tokenizer
    ):
        """
        target: test create collection with full text search with unsupported tokenizer
        method: create collection with full text search, use bm25 function and unsupported tokenizer
        expected: create collection failed
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
            FieldSchema(
                name="paragraph_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR
            ),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        text_fields = ["text", "paragraph"]
        for field in text_fields:
            bm25_function = Function(
                name=f"{field}_bm25_emb",
                function_type=FunctionType.BM25,
                input_field_names=[field],
                output_field_names=[f"{field}_sparse_emb"],
                params={},
            )
            schema.add_function(bm25_function)
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        res, result = collection_w.describe()
        log.info(f"collection describe {res}")
        assert not result, (
            "create collection with unsupported tokenizer should be failed"
        )

    @pytest.mark.tags(CaseLabel.L2)
    @pytest.mark.parametrize("valid_output", [True, False])
    @pytest.mark.parametrize("valid_input", [True, False])
    def test_create_collection_for_full_text_search_with_invalid_input_output(
        self, valid_output, valid_input
    ):
        """
        target: test create collection with full text search with invalid input/output in bm25 function
        method: create collection with full text search, use bm25 function and invalid input/output
        expected: create collection failed
        """
        analyzer_params = {
            "tokenizer": "standard",
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
            FieldSchema(
                name="paragraph_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR
            ),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        if valid_input:
            input_field_names = ["text"]
        else:
            input_field_names = ["invalid_inout"]
        if valid_output:
            output_field_names = ["text_sparse_emb"]
        else:
            output_field_names = ["invalid_output"]

        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=input_field_names,
            output_field_names=output_field_names,
            params={},
        )
        schema.add_function(bm25_function)
        if (not valid_output) or (not valid_input):
            self.init_collection_wrap(
                name=cf.gen_unique_str(prefix),
                schema=schema,
                check_task=CheckTasks.err_res,
                check_items={
                    ct.err_code: 1,
                    ct.err_msg: "field not found in collection",
                },
            )
        else:
            collection_w = self.init_collection_wrap(
                name=cf.gen_unique_str(prefix), schema=schema
            )
            res, result = collection_w.describe()
            log.info(f"collection describe {res}")
            assert result, (
                "create collection with valid input/output should be successful"
            )

    @pytest.mark.tags(CaseLabel.L1)
    def test_create_collection_for_full_text_search_with_field_not_tokenized(self):
        """
        target: test create collection with full text search with field not tokenized
        method: create collection with full text search, use bm25 function and input field not tokenized
        expected: create collection failed
        """
        analyzer_params = {
            "tokenizer": "standard",
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=False,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
            FieldSchema(
                name="paragraph_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR
            ),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")

        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        check_task = CheckTasks.err_res
        check_items = {
            ct.err_code: 65535,
            ct.err_msg: "BM25 function input field must set enable_analyzer to true",
        }
        self.init_collection_wrap(
            name=cf.gen_unique_str(prefix),
            schema=schema,
            check_task=check_task,
            check_items=check_items,
        )


# @pytest.mark.skip("skip")
class TestInsertWithFullTextSearch(TestcaseBase):
    """
    ******************************************************************
        The following cases are used to test insert with full text search
    ******************************************************************
    """

    @pytest.mark.tags(CaseLabel.L0)
    @pytest.mark.parametrize("nullable", [False, True])
    @pytest.mark.parametrize("text_lang", ["en", "zh", "hybrid"])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_insert_for_full_text_search_default(self, tokenizer, text_lang, nullable):
        """
        target: test insert data with full text search
        method: 1. insert data with varchar in different language
                2. query count and verify the result
        expected: insert successfully and count is correct
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                nullable=nullable,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                nullable=nullable,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        if text_lang == "zh":
            fake = fake_zh
        elif text_lang == "hybrid":
            fake = Faker()

        if nullable:
            data = [
                {
                    "id": i,
                    "word": fake.word().lower(),
                    "sentence": fake.sentence().lower()
                    if random.random() < 0.5
                    else None,
                    "paragraph": fake.paragraph().lower()
                    if random.random() < 0.5
                    else None,
                    "text": fake.text().lower(),  # function input should not be None
                    "emb": [random.random() for _ in range(dim)],
                }
                for i in range(data_size)
            ]
        else:
            data = [
                {
                    "id": i,
                    "word": fake.word().lower(),
                    "sentence": fake.sentence().lower(),
                    "paragraph": fake.paragraph().lower(),
                    "text": fake.text().lower(),
                    "emb": [random.random() for _ in range(dim)],
                }
                for i in range(data_size)
            ]
        if text_lang == "hybrid":
            hybrid_data = []
            for i in range(data_size):
                fake = random.choice([fake_en, fake_zh, Faker("de_DE")])
                tmp = {
                    "id": i,
                    "word": fake.word().lower(),
                    "sentence": fake.sentence().lower(),
                    "paragraph": fake.paragraph().lower(),
                    "text": fake.text().lower(),
                    "emb": [random.random() for _ in range(dim)],
                }
                hybrid_data.append(tmp)
            data = hybrid_data + data
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": "SPARSE_INVERTED_INDEX",
                "metric_type": "BM25",
                "params": {
                    "drop_ratio_build": 0.3,
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                },
            },
        )
        collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        num_entities = collection_w.num_entities
        res, _ = collection_w.query(expr="", output_fields=["count(*)"])
        count = res[0]["count(*)"]
        assert len(data) == num_entities
        assert len(data) == count

    @pytest.mark.tags(CaseLabel.L0)
    @pytest.mark.parametrize("enable_dynamic_field", [True])
    @pytest.mark.parametrize("nullable", [False])
    @pytest.mark.parametrize("text_lang", ["en"])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_insert_for_full_text_search_enable_dynamic_field(
        self, tokenizer, text_lang, nullable, enable_dynamic_field
    ):
        """
        target: test insert data with full text search and enable dynamic field
        method: 1. create collection with full text search and enable dynamic field
                2. insert data with varchar
                3. query count and verify the result
        expected: insert successfully and count is correct
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                nullable=nullable,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                nullable=nullable,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(
            fields=fields,
            description="test collection",
            enable_dynamic_field=enable_dynamic_field,
        )
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        if text_lang == "zh":
            fake = fake_zh
        elif text_lang == "de":
            fake = Faker("de_DE")
        elif text_lang == "hybrid":
            fake = Faker()

        if nullable:
            data = [
                {
                    "id": i,
                    "word": fake.word().lower(),
                    "sentence": fake.sentence().lower()
                    if random.random() < 0.5
                    else None,
                    "paragraph": fake.paragraph().lower()
                    if random.random() < 0.5
                    else None,
                    "text": fake.text().lower(),  # function input should not be None
                    "emb": [random.random() for _ in range(dim)],
                    f"dynamic_field_{i}": f"dynamic_value_{i}",
                }
                for i in range(data_size)
            ]
        else:
            data = [
                {
                    "id": i,
                    "word": fake.word().lower(),
                    "sentence": fake.sentence().lower(),
                    "paragraph": fake.paragraph().lower(),
                    "text": fake.text().lower(),
                    "emb": [random.random() for _ in range(dim)],
                    f"dynamic_field_{i}": f"dynamic_value_{i}",
                }
                for i in range(data_size)
            ]
        if text_lang == "hybrid":
            hybrid_data = []
            for i in range(data_size):
                fake = random.choice([fake_en, fake_zh, Faker("de_DE")])
                tmp = {
                    "id": i,
                    "word": fake.word().lower(),
                    "sentence": fake.sentence().lower(),
                    "paragraph": fake.paragraph().lower(),
                    "text": fake.text().lower(),
                    "emb": [random.random() for _ in range(dim)],
                    f"dynamic_field_{i}": f"dynamic_value_{i}",
                }
                hybrid_data.append(tmp)
            data = hybrid_data + data
        # df = pd.DataFrame(data)
        # log.info(f"dataframe\n{df}")
        batch_size = 5000
        for i in range(0, len(data), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(data)
                else data[i : len(data)]
            )
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": "SPARSE_INVERTED_INDEX",
                "metric_type": "BM25",
                "params": {
                    "drop_ratio_build": 0.3,
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                },
            },
        )
        collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        num_entities = collection_w.num_entities
        res, _ = collection_w.query(expr="", output_fields=["count(*)"])
        count = res[0]["count(*)"]
        assert len(data) == num_entities
        assert len(data) == count

    @pytest.mark.tags(CaseLabel.L0)
    @pytest.mark.parametrize("nullable", [True])
    @pytest.mark.parametrize("text_lang", ["en"])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_insert_for_full_text_search_with_dataframe(
        self, tokenizer, text_lang, nullable
    ):
        """
        target: test insert data for full text search with dataframe
        method: 1. insert data with varchar in dataframe format
                2. query count and verify the result
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                nullable=nullable,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                nullable=nullable,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        if text_lang == "zh":
            fake = fake_zh
        elif text_lang == "de":
            fake = Faker("de_DE")
        elif text_lang == "hybrid":
            fake = Faker()

        if nullable:
            data = [
                {
                    "id": i,
                    "word": fake.word().lower(),
                    "sentence": fake.sentence().lower()
                    if random.random() < 0.5
                    else None,
                    "paragraph": fake.paragraph().lower()
                    if random.random() < 0.5
                    else None,
                    "text": fake.text().lower(),  # function input should not be None
                    "emb": [random.random() for _ in range(dim)],
                }
                for i in range(data_size)
            ]
        else:
            data = [
                {
                    "id": i,
                    "word": fake.word().lower(),
                    "sentence": fake.sentence().lower(),
                    "paragraph": fake.paragraph().lower(),
                    "text": fake.text().lower(),
                    "emb": [random.random() for _ in range(dim)],
                }
                for i in range(data_size)
            ]
        if text_lang == "hybrid":
            hybrid_data = []
            for i in range(data_size):
                fake = random.choice([fake_en, fake_zh, Faker("de_DE")])
                tmp = {
                    "id": i,
                    "word": fake.word().lower(),
                    "sentence": fake.sentence().lower(),
                    "paragraph": fake.paragraph().lower(),
                    "text": fake.text().lower(),
                    "emb": [random.random() for _ in range(dim)],
                }
                hybrid_data.append(tmp)
            data = hybrid_data + data
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(df[i : i + batch_size])
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": "SPARSE_INVERTED_INDEX",
                "metric_type": "BM25",
                "params": {
                    "drop_ratio_build": 0.3,
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                },
            },
        )
        collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        num_entities = collection_w.num_entities
        res, _ = collection_w.query(expr="", output_fields=["count(*)"])
        count = res[0]["count(*)"]
        assert len(data) == num_entities
        assert len(data) == count

    @pytest.mark.tags(CaseLabel.L2)
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_insert_for_full_text_search_with_part_of_empty_string(self, tokenizer):
        """
        target: test insert data with full text search with part of empty string
        method: 1. insert data with part of empty string
                2. query count and verify the result
                3. search with text
        expected: insert successfully, count is correct, and search result is correct
        """

        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        log.info(f"collection describe {collection_w.describe()}")
        fake = fake_en
        language = "en"
        if tokenizer == "jieba":
            fake = fake_zh
            language = "zh"
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": "SPARSE_INVERTED_INDEX",
                "metric_type": "BM25",
                "params": {
                    "drop_ratio_build": 0.3,
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                },
            },
        )
        collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        data = [
            {
                "id": i,
                "word": fake.word().lower() if random.random() < 0.5 else "",
                "sentence": fake.sentence().lower() if random.random() < 0.5 else "",
                "paragraph": fake.paragraph().lower() if random.random() < 0.5 else "",
                "text": fake.text().lower() if random.random() < 0.5 else "",
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        log.info("analyze documents")
        texts = df["text"].to_list()
        word_freq = cf.analyze_documents(texts, language=language)
        tokens = list(word_freq.keys())
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        num_entities = collection_w.num_entities
        # query with count(*)
        res, _ = collection_w.query(expr="", output_fields=["count(*)"])
        count = res[0]["count(*)"]
        assert len(data) == num_entities
        assert len(data) == count
        # query with expr
        res, _ = collection_w.query(expr="id >= 0", output_fields=["text"])
        assert len(res) == len(data)

        # search with text
        nq = 2
        limit = 100
        search_data = [fake.text().lower() + random.choice(tokens) for _ in range(nq)]
        res_list, _ = collection_w.search(
            data=search_data,
            anns_field="text_sparse_emb",
            param={},
            limit=limit,
            output_fields=["id", "text"],
        )
        assert len(res_list) == nq
        for i in range(nq):
            assert len(res_list[i]) == limit
            search_text = search_data[i]
            log.info(f"res: {res_list[i]}")
            res = res_list[i]
            for j in range(len(res)):
                r = res[j]
                result_text = r.text
                overlap, word_freq_a, word_freq_b = cf.check_token_overlap(
                    search_text, result_text, language=language
                )
                assert len(overlap) > 0, (
                    f"query text: {search_text}, \ntext: {result_text} \n overlap: {overlap} \n word freq a: {word_freq_a} \n word freq b: {word_freq_b}\n result: {r}"
                )


# @pytest.mark.skip("skip")
class TestInsertWithFullTextSearchNegative(TestcaseBase):
    """
    ******************************************************************
        The following cases are used to test insert with full text search negative
    ******************************************************************
    """

    @pytest.mark.tags(CaseLabel.L1)
    @pytest.mark.parametrize("nullable", [True])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_insert_with_full_text_search_with_non_varchar_data(
        self, tokenizer, nullable
    ):
        """
        target: test insert data with full text search with non varchar data
        method: 1. insert data with non varchar data
        expected: insert failed
        """

        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                nullable=nullable,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                nullable=nullable,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        if tokenizer == "jieba":
            fake = fake_zh

        data = [
            {
                "id": i,
                "word": fake.word().lower(),
                "sentence": fake.sentence().lower(),
                "paragraph": fake.paragraph().lower(),
                "text": fake.text().lower()
                if random.random() < 0.5
                else 1,  # mix some int data
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)],
                check_task=CheckTasks.err_res,
                check_items={
                    ct.err_code: 1,
                    ct.err_msg: "inconsistent with defined schema",
                },
            )


# @pytest.mark.skip("skip")
class TestUpsertWithFullTextSearch(TestcaseBase):
    """
    ******************************************************************
        The following cases are used to test upsert with full text search
    ******************************************************************
    """

    @pytest.mark.tags(CaseLabel.L0)
    @pytest.mark.parametrize("nullable", [False, True])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_upsert_for_full_text_search(self, tokenizer, nullable):
        """
        target: test upsert data for full text search
        method: 1. insert data with varchar
                2. upsert in half of the data
                3. check the data
        expected: upsert successfully and data is updated
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                nullable=nullable,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                nullable=nullable,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        if tokenizer == "jieba":
            fake = fake_zh

        if nullable:
            data = [
                {
                    "id": i,
                    "word": fake.word().lower(),
                    "sentence": fake.sentence().lower()
                    if random.random() < 0.5
                    else None,
                    "paragraph": fake.paragraph().lower()
                    if random.random() < 0.5
                    else None,
                    "text": fake.text().lower(),  # function input should not be None
                    "emb": [random.random() for _ in range(dim)],
                }
                for i in range(data_size)
            ]
        else:
            data = [
                {
                    "id": i,
                    "word": fake.word().lower(),
                    "sentence": fake.sentence().lower(),
                    "paragraph": fake.paragraph().lower(),
                    "text": fake.text().lower(),
                    "emb": [random.random() for _ in range(dim)],
                }
                for i in range(data_size)
            ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": "SPARSE_INVERTED_INDEX",
                "metric_type": "BM25",
                "params": {
                    "drop_ratio_build": 0.3,
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                },
            },
        )
        collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        num_entities = collection_w.num_entities
        res, _ = collection_w.query(expr="", output_fields=["count(*)"])
        count = res[0]["count(*)"]
        assert len(data) == num_entities
        assert len(data) == count

        # upsert in half of the data
        upsert_data = [
            {
                "id": i,
                "word": fake.word().lower(),
                "sentence": fake.sentence().lower(),
                "paragraph": fake.paragraph().lower(),
                "text": fake.text().lower(),
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size // 2)
        ]
        upsert_data += data[data_size // 2 :]
        for i in range(0, len(upsert_data), batch_size):
            collection_w.upsert(
                upsert_data[i : i + batch_size]
                if i + batch_size < len(upsert_data)
                else upsert_data[i : len(upsert_data)]
            )
        res, _ = collection_w.query(expr="id >= 0", output_fields=["*"])
        upsert_data_map = {}
        for d in upsert_data:
            upsert_data_map[d["id"]] = d
        for r in res:
            _id = r["id"]
            word = r["word"]
            assert word == upsert_data_map[_id]["word"]


# @pytest.mark.skip("skip")
class TestUpsertWithFullTextSearchNegative(TestcaseBase):
    """
    ******************************************************************
        The following cases are used to test upsert data in full text search with negative condition
    ******************************************************************
    """

    @pytest.mark.tags(CaseLabel.L1)
    @pytest.mark.parametrize("nullable", [False])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_upsert_for_full_text_search_with_no_varchar_data(
        self, tokenizer, nullable
    ):
        """
        target: test upsert data for full text search with no varchar data
        method: 1. insert data with varchar data
                2. upsert in half of the data with some data is int
        expected: upsert failed
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                nullable=nullable,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                nullable=nullable,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        if tokenizer == "jieba":
            fake = fake_zh

        data = [
            {
                "id": i,
                "word": fake.word().lower(),
                "sentence": fake.sentence().lower(),
                "paragraph": fake.paragraph().lower(),
                "text": fake.text().lower(),
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": "SPARSE_INVERTED_INDEX",
                "metric_type": "BM25",
                "params": {
                    "drop_ratio_build": 0.3,
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                },
            },
        )
        collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        num_entities = collection_w.num_entities
        res, _ = collection_w.query(expr="", output_fields=["count(*)"])
        count = res[0]["count(*)"]
        assert len(data) == num_entities
        assert len(data) == count

        # upsert in half of the data
        upsert_data = [
            {
                "id": i,
                "word": fake.word().lower(),
                "sentence": fake.sentence().lower(),
                "paragraph": fake.paragraph().lower(),
                "text": fake.text().lower()
                if random.random() < 0.5
                else 1,  # mix some int data
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        check_items = {ct.err_code: 1, ct.err_msg: "inconsistent with defined schema"}
        check_task = CheckTasks.err_res
        collection_w.upsert(upsert_data, check_task=check_task, check_items=check_items)


class TestDeleteWithFullTextSearch(TestcaseBase):
    """
    ******************************************************************
        The following cases are used to test delete data in full text search
    ******************************************************************
    """

    @pytest.mark.tags(CaseLabel.L1)
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_delete_for_full_text_search(self, tokenizer):
        """
        target: test delete data for full text search
        method: 1. insert data with varchar
                2. delete half of the data
                3. check the data
        expected: delete successfully and data is deleted
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        if tokenizer == "jieba":
            fake = fake_zh
        data = [
            {
                "id": i,
                "word": fake.word().lower(),
                "sentence": fake.sentence().lower(),
                "paragraph": fake.paragraph().lower(),
                "text": fake.text().lower(),
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": "SPARSE_INVERTED_INDEX",
                "metric_type": "BM25",
                "params": {
                    "drop_ratio_build": 0.3,
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                },
            },
        )
        collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        num_entities = collection_w.num_entities
        res, _ = collection_w.query(expr="", output_fields=["count(*)"])
        count = res[0]["count(*)"]
        assert len(data) == num_entities
        assert len(data) == count

        # delete half of the data
        delete_ids = [i for i in range(data_size // 2)]
        collection_w.delete(expr=f"id in {delete_ids}")
        res, _ = collection_w.query(expr="", output_fields=["count(*)"])
        count = res[0]["count(*)"]
        assert count == data_size // 2

        # query with delete expr and get empty result
        res, _ = collection_w.query(expr=f"id in {delete_ids}", output_fields=["*"])
        assert len(res) == 0

        # search with text has been deleted, not in the result
        search_data = df["text"].to_list()[: data_size // 2]
        res_list, _ = collection_w.search(
            data=search_data,
            anns_field="text_sparse_emb",
            param={},
            limit=100,
            output_fields=["id", "text"],
        )
        for i in range(len(res_list)):
            query_text = search_data[i]
            result_texts = [r.text for r in res_list[i]]
            assert query_text not in result_texts


class TestDeleteWithFullTextSearchNegative(TestcaseBase):
    """
    todo: add some negative cases
    """

    pass


# @pytest.mark.skip("skip")
class TestCreateIndexWithFullTextSearch(TestcaseBase):
    """
    ******************************************************************
      The following cases are used to test full text search in index creation
    ******************************************************************
    """

    @pytest.mark.tags(CaseLabel.L1)
    @pytest.mark.parametrize("b", [0.1])
    @pytest.mark.parametrize("k", [1.2])
    @pytest.mark.parametrize("index_type", ["SPARSE_INVERTED_INDEX", "SPARSE_WAND"])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_create_index_for_full_text_search_default(
        self, tokenizer, index_type, k, b
    ):
        """
        target: test create index for full text search
        method: 1. enable full text search and insert data with varchar
                2. create index for full text search with different index type
                3. verify the index info by describe index
        expected: create index successfully and index info is correct
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        empty_percent = 0.0
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                enable_match=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        data = [
            {
                "id": i,
                "word": fake.word().lower() if random.random() >= empty_percent else "",
                "sentence": fake.sentence().lower()
                if random.random() >= empty_percent
                else "",
                "paragraph": fake.paragraph().lower()
                if random.random() >= empty_percent
                else "",
                "text": fake.text().lower() if random.random() >= empty_percent else "",
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": index_type,
                "metric_type": "BM25",
                "params": {
                    "bm25_k1": k,
                    "bm25_b": b,
                },
            },
        )
        # describe index info to verify
        res = collection_w.indexes
        index_info = [r.to_dict() for r in res]
        log.info(f"index info: {index_info}")
        for info in index_info:
            if info["index_name"] == "text_sparse_emb":
                assert info["index_param"]["index_type"] == index_type
                assert info["index_param"]["metric_type"] == "BM25"
                assert info["index_param"]["params"]["bm25_k1"] == k
                assert info["index_param"]["params"]["bm25_b"] == b
                break


class TestCreateIndexWithFullTextSearchNegative(TestcaseBase):
    """
    ******************************************************************
      The following cases are used to test full text search in index creation negative
    ******************************************************************
    """

    @pytest.mark.tags(CaseLabel.L2)
    @pytest.mark.parametrize("b", [0.5])
    @pytest.mark.parametrize("k", [1.5])
    @pytest.mark.parametrize("index_type", ["HNSW", "INVALID_INDEX_TYPE"])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_create_full_text_search_with_invalid_index_type(
        self, tokenizer, index_type, k, b
    ):
        """
        target: test create index for full text search with invalid index type
        method: 1. enable full text search and insert data with varchar
                2. create index for full text search with invalid index type
        expected: create index failed
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        empty_percent = 0.0
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                enable_match=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        data = [
            {
                "id": i,
                "word": fake.word().lower() if random.random() >= empty_percent else "",
                "sentence": fake.sentence().lower()
                if random.random() >= empty_percent
                else "",
                "paragraph": fake.paragraph().lower()
                if random.random() >= empty_percent
                else "",
                "text": fake.text().lower() if random.random() >= empty_percent else "",
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        error = {"err_code": 1100, "err_msg": "invalid"}
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": index_type,
                "metric_type": "BM25",
                "params": {
                    "bm25_k1": k,
                    "bm25_b": b,
                },
            },
            check_task=CheckTasks.err_res,
            check_items=error,
        )

    @pytest.mark.tags(CaseLabel.L2)
    @pytest.mark.parametrize("b", [0.5])
    @pytest.mark.parametrize("k", [1.5])
    @pytest.mark.parametrize("index_type", ["SPARSE_INVERTED_INDEX"])
    @pytest.mark.parametrize("metric_type", ["COSINE", "L2", "IP"])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_create_full_text_search_index_with_invalid_metric_type(
        self, tokenizer, index_type, metric_type, k, b
    ):
        """
        target: test create index for full text search with invalid metric type
        method: 1. enable full text search and insert data with varchar
                2. create index for full text search with invalid metric type
        expected: create index failed
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        empty_percent = 0.0
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                enable_match=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        data = [
            {
                "id": i,
                "word": fake.word().lower() if random.random() >= empty_percent else "",
                "sentence": fake.sentence().lower()
                if random.random() >= empty_percent
                else "",
                "paragraph": fake.paragraph().lower()
                if random.random() >= empty_percent
                else "",
                "text": fake.text().lower() if random.random() >= empty_percent else "",
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        error = {
            ct.err_code: 65535,
            ct.err_msg: "index metric type of BM25 function output field must be BM25",
        }
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": index_type,
                "metric_type": metric_type,
                "params": {
                    "bm25_k1": k,
                    "bm25_b": b,
                },
            },
            check_task=CheckTasks.err_res,
            check_items=error,
        )

    @pytest.mark.tags(CaseLabel.L2)
    @pytest.mark.parametrize("b", [0.5])
    @pytest.mark.parametrize("k", [1.5])
    @pytest.mark.parametrize("index_type", ["SPARSE_INVERTED_INDEX"])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_create_index_using_bm25_metric_type_for_non_bm25_output_field(
        self, tokenizer, index_type, k, b
    ):
        """
        target: test create index using bm25 metric type for non bm25 output field (dense float vector or
                sparse float vector not for bm25)
        method: 1. enable full text search and insert data with varchar
                2. create index using bm25 metric type for non bm25 output field
        expected: create index failed
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        empty_percent = 0.0
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                enable_match=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        data = [
            {
                "id": i,
                "word": fake.word().lower() if random.random() >= empty_percent else "",
                "sentence": fake.sentence().lower()
                if random.random() >= empty_percent
                else "",
                "paragraph": fake.paragraph().lower()
                if random.random() >= empty_percent
                else "",
                "text": fake.text().lower() if random.random() >= empty_percent else "",
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        error = {
            ct.err_code: 1100,
            ct.err_msg: "float vector index does not support metric type: BM25",
        }
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "BM25",
                "params": {"M": 16, "efConstruction": 500},
            },
            check_task=CheckTasks.err_res,
            check_items=error,
        )

    @pytest.mark.tags(CaseLabel.L0)
    @pytest.mark.parametrize("b", [-1])
    @pytest.mark.parametrize("k", [-1])
    @pytest.mark.parametrize("index_type", ["SPARSE_INVERTED_INDEX"])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_create_full_text_search_with_invalid_bm25_params(
        self, tokenizer, index_type, k, b
    ):
        """
        target: test create index for full text search with invalid bm25 params
        method: 1. enable full text search and insert data with varchar
                2. create index for full text search with invalid bm25 params
        expected: create index failed
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        empty_percent = 0.0
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=True,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                enable_match=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        data = [
            {
                "id": i,
                "word": fake.word().lower() if random.random() >= empty_percent else "",
                "sentence": fake.sentence().lower()
                if random.random() >= empty_percent
                else "",
                "paragraph": fake.paragraph().lower()
                if random.random() >= empty_percent
                else "",
                "text": fake.text().lower() if random.random() >= empty_percent else "",
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )

        check_task = CheckTasks.err_res
        error = {
            "err_code": 1100,
            "err_msg": "invalid",
        }  # todo, update error code and message
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": index_type,
                "metric_type": "BM25",
                "params": {
                    "bm25_k1": k,
                    "bm25_b": b,
                },
            },
            check_task=check_task,
            check_items=error,
        )


# @pytest.mark.skip("skip")
class TestSearchWithFullTextSearch(TestcaseBase):
    """
    ******************************************************************
      The following cases are used to test search for full text search
    ******************************************************************
    """

    @pytest.mark.tags(CaseLabel.L0)
    @pytest.mark.parametrize("nq", [2])
    @pytest.mark.parametrize("empty_percent", [0.5])
    @pytest.mark.parametrize("enable_partition_key", [True])
    @pytest.mark.parametrize("enable_inverted_index", [True])
    @pytest.mark.parametrize("index_type", ["SPARSE_INVERTED_INDEX", "SPARSE_WAND"])
    @pytest.mark.parametrize("expr", ["text_match", "id_range"])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    @pytest.mark.parametrize("offset", [10, 0])
    def test_full_text_search_default(
        self,
        offset,
        tokenizer,
        expr,
        enable_inverted_index,
        enable_partition_key,
        empty_percent,
        index_type,
        nq,
    ):
        """
        target: test full text search
        method: 1. enable full text search and insert data with varchar
                2. search with text
                3. verify the result
        expected: full text search successfully and result is correct
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=enable_partition_key,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                enable_match=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        if tokenizer == "jieba":
            language = "zh"
            fake = fake_zh
        else:
            language = "en"

        data = [
            {
                "id": i,
                "word": fake.word().lower() if random.random() >= empty_percent else "",
                "sentence": fake.sentence().lower()
                if random.random() >= empty_percent
                else "",
                "paragraph": fake.paragraph().lower()
                if random.random() >= empty_percent
                else "",
                "text": fake.text().lower() if random.random() >= empty_percent else "",
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        texts = df["text"].to_list()
        word_freq = cf.analyze_documents(texts, language=language)
        most_freq_word = word_freq.most_common(10)
        tokens = [item[0] for item in most_freq_word]
        if len(tokens) == 0:
            log.info("empty tokens, add a dummy token")
            tokens = ["dummy"]
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.flush()
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": index_type,
                "metric_type": "BM25",
                "params": {
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                },
            },
        )
        if enable_inverted_index:
            collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        limit = 100
        token = random.choice(tokens)
        search_data = [fake.text().lower() + f" {token} " for _ in range(nq)]
        if expr == "text_match":
            filter = f"TEXT_MATCH(text, '{token}')"
            res, _ = collection_w.query(
                expr=filter,
            )
        elif expr == "id_range":
            filter = f"id < {data_size // 2}"
        else:
            filter = ""
        res, _ = collection_w.query(
            expr=filter,
            limit=limit,
        )
        candidates_num = len(res)
        log.info(f"search data: {search_data}")
        # use offset = 0 to get all the results
        full_res_list, _ = collection_w.search(
            data=search_data,
            anns_field="text_sparse_emb",
            expr=filter,
            param={},
            limit=limit + offset,
            offset=0,
            output_fields=["id", "text"],
        )
        full_res_id_list = []
        for i in range(nq):
            res = full_res_list[i]
            tmp = []
            for r in res:
                tmp.append(r.id)
            full_res_id_list.append(tmp)

        res_list, _ = collection_w.search(
            data=search_data,
            anns_field="text_sparse_emb",
            expr=filter,
            param={},
            limit=limit,
            offset=offset,
            output_fields=["id", "text"],
        )

        # verify correctness
        for i in range(nq):
            assert 0 < len(res_list[i]) <= min(limit, candidates_num)
            search_text = search_data[i]
            log.info(f"res: {res_list[i]}")
            res = res_list[i]
            for j in range(len(res)):
                r = res[j]
                _id = r.id
                # get the first id of the result in which position is larger than offset
                if j == 0:
                    first_id = _id
                    p = full_res_id_list[i].index(first_id)
                    assert 1.2 * offset >= p >= offset * 0.8
                result_text = r.text
                # verify search result satisfies the filter
                if expr == "text_match":
                    assert token in result_text
                if expr == "id_range":
                    assert _id < data_size // 2
                # verify search result has overlap with search text
                overlap, word_freq_a, word_freq_b = cf.check_token_overlap(
                    search_text, result_text, language=language
                )
                log.info(f"overlap {overlap}")
                assert len(overlap) > 0, (
                    f"query text: {search_text}, \ntext: {result_text} \n overlap: {overlap} \n word freq a: {word_freq_a} \n word freq b: {word_freq_b}\n result: {r}"
                )

    @pytest.mark.tags(CaseLabel.L0)
    @pytest.mark.parametrize("nq", [2])
    @pytest.mark.parametrize("empty_percent", [0.5])
    @pytest.mark.parametrize("enable_partition_key", [True])
    @pytest.mark.parametrize("enable_inverted_index", [True])
    @pytest.mark.parametrize("index_type", ["SPARSE_INVERTED_INDEX"])
    @pytest.mark.parametrize("expr", ["text_match"])
    @pytest.mark.parametrize("offset", [10])
    @pytest.mark.parametrize("tokenizer", ["jieba"])
    @pytest.mark.parametrize("inverted_index_algo", ct.inverted_index_algo)
    def test_full_text_search_with_jieba_tokenizer(
        self,
        offset,
        tokenizer,
        expr,
        enable_inverted_index,
        enable_partition_key,
        empty_percent,
        index_type,
        nq,
        inverted_index_algo,
    ):
        """
        target: test full text search
        method: 1. enable full text search with jieba tokenizer and insert data with varchar
                2. search with text
                3. verify the result
        expected: full text search successfully and result is correct
        """
        if tokenizer == "jieba":
            lang_type = "chinese"
        else:
            lang_type = "english"

        analyzer_params = {
            "type": lang_type,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=enable_partition_key,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                enable_match=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        if tokenizer == "jieba":
            language = "zh"
            fake = fake_zh
        else:
            language = "en"

        data = [
            {
                "id": i,
                "word": fake.word().lower() if random.random() >= empty_percent else "",
                "sentence": fake.sentence().lower()
                if random.random() >= empty_percent
                else "",
                "paragraph": fake.paragraph().lower()
                if random.random() >= empty_percent
                else "",
                "text": fake.text().lower() if random.random() >= empty_percent else "",
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        texts = df["text"].to_list()
        word_freq = cf.analyze_documents(texts, language=language)
        tokens = []
        for item in word_freq.most_common(20):
            if len(item[0]) == 2:
                tokens.append(item[0])
        if len(tokens) == 0:
            log.info("empty tokens, add a dummy token")
            tokens = ["dummy"]
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.flush()
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": index_type,
                "metric_type": "BM25",
                "params": {
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                    "inverted_index_algo": inverted_index_algo,
                },
            },
        )
        if enable_inverted_index:
            collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        limit = 100
        token = random.choice(tokens)
        search_data = [fake.text().lower() + " " + token for _ in range(nq)]
        if expr == "text_match":
            filter = f"text_match(text, '{token}')"
            res, _ = collection_w.query(
                expr=filter,
            )
        elif expr == "id_range":
            filter = f"id < {data_size // 2}"
        else:
            filter = ""
        res, _ = collection_w.query(
            expr=filter,
            limit=limit,
        )
        candidates_num = len(res)
        log.info(f"search data: {search_data}")
        # use offset = 0 to get all the results
        full_res_list, _ = collection_w.search(
            data=search_data,
            anns_field="text_sparse_emb",
            expr=filter,
            param={},
            limit=limit + offset,
            offset=0,
            output_fields=["id", "text"],
        )
        full_res_id_list = []
        for i in range(nq):
            res = full_res_list[i]
            tmp = []
            for r in res:
                tmp.append(r.id)
            full_res_id_list.append(tmp)

        res_list, _ = collection_w.search(
            data=search_data,
            anns_field="text_sparse_emb",
            expr=filter,
            param={},
            limit=limit,
            offset=offset,
            output_fields=["id", "text"],
        )

        # verify correctness
        for i in range(nq):
            assert 0 < len(res_list[i]) <= min(limit, candidates_num)
            search_text = search_data[i]
            log.info(f"res: {res_list[i]}")
            res = res_list[i]
            for j in range(len(res)):
                r = res[j]
                _id = r.id
                # get the first id of the result in which position is larger than offset
                if j == 0:
                    first_id = _id
                    p = full_res_id_list[i].index(first_id)
                    assert 1.2 * offset >= p >= offset * 0.8
                result_text = r.text
                # verify search result satisfies the filter
                if expr == "text_match":
                    assert token in result_text
                if expr == "id_range":
                    assert _id < data_size // 2
                # verify search result has overlap with search text
                overlap, word_freq_a, word_freq_b = cf.check_token_overlap(
                    search_text, result_text, language=language
                )
                log.info(f"overlap {overlap}")
                assert len(overlap) > 0, (
                    f"query text: {search_text}, \ntext: {result_text} \n overlap: {overlap} \n word freq a: {word_freq_a} \n word freq b: {word_freq_b}\n result: {r}"
                )

    @pytest.mark.tags(CaseLabel.L0)
    @pytest.mark.parametrize("nq", [2])
    @pytest.mark.parametrize("empty_percent", [0.5])
    @pytest.mark.parametrize("enable_partition_key", [True])
    @pytest.mark.parametrize("enable_inverted_index", [True])
    @pytest.mark.parametrize("index_type", ["SPARSE_INVERTED_INDEX"])
    @pytest.mark.parametrize("expr", ["id_range"])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    @pytest.mark.parametrize("offset", [0])
    def test_full_text_search_for_growing_segment(
        self,
        offset,
        tokenizer,
        expr,
        enable_inverted_index,
        enable_partition_key,
        empty_percent,
        index_type,
        nq,
    ):
        """
        target: test full text search
        method: 1. enable full text search and insert data with varchar
                2. search with text
                3. verify the result
        expected: full text search successfully and result is correct
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=enable_partition_key,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                enable_match=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        if tokenizer == "jieba":
            language = "zh"
            fake = fake_zh
        else:
            language = "en"

        data = [
            {
                "id": i,
                "word": fake.word().lower() if random.random() >= empty_percent else "",
                "sentence": fake.sentence().lower()
                if random.random() >= empty_percent
                else "",
                "paragraph": fake.paragraph().lower()
                if random.random() >= empty_percent
                else "",
                "text": fake.text().lower() if random.random() >= empty_percent else "",
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        texts = df["text"].to_list()
        word_freq = cf.analyze_documents(texts, language=language)
        most_freq_word = word_freq.most_common(10)
        tokens = [item[0] for item in most_freq_word]
        if len(tokens) == 0:
            log.info("empty tokens, add a dummy token")
            tokens = ["dummy"]
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": index_type,
                "metric_type": "BM25",
                "params": {
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                },
            },
        )
        if enable_inverted_index:
            collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        limit = 100
        search_data = [
            fake.text().lower() + " " + random.choice(tokens) for _ in range(nq)
        ]
        if expr == "text_match":
            filter = f"TextMatch(text, '{tokens[0]}')"
            res, _ = collection_w.query(
                expr=filter,
            )
        elif expr == "id_range":
            filter = f"id < {data_size // 2}"
        else:
            filter = ""
        res, _ = collection_w.query(
            expr=filter,
            limit=limit,
        )
        candidates_num = len(res)
        log.info(f"search data: {search_data}")
        # use offset = 0 to get all the results
        full_res_list, _ = collection_w.search(
            data=search_data,
            anns_field="text_sparse_emb",
            expr=filter,
            param={},
            limit=limit + offset,
            offset=0,
            output_fields=["id", "text"],
        )
        full_res_id_list = []
        for i in range(nq):
            res = full_res_list[i]
            tmp = []
            for r in res:
                tmp.append(r.id)
            full_res_id_list.append(tmp)

        res_list, _ = collection_w.search(
            data=search_data,
            anns_field="text_sparse_emb",
            expr=filter,
            param={},
            limit=limit,
            offset=offset,
            output_fields=["id", "text"],
        )

        # verify correctness
        for i in range(nq):
            assert 0 < len(res_list[i]) <= min(limit, candidates_num)
            search_text = search_data[i]
            log.info(f"res: {res_list[i]}")
            res = res_list[i]
            for j in range(len(res)):
                r = res[j]
                _id = r.id
                # get the first id of the result in which position is larger than offset
                if j == 0:
                    first_id = _id
                    p = full_res_id_list[i].index(first_id)
                    assert 1.2 * offset >= p >= offset * 0.8
                result_text = r.text
                # verify search result satisfies the filter
                if expr == "text_match":
                    assert tokens[0] in result_text
                if expr == "id_range":
                    assert _id < data_size // 2
                # verify search result has overlap with search text
                overlap, word_freq_a, word_freq_b = cf.check_token_overlap(
                    search_text, result_text, language=language
                )
                log.info(f"overlap {overlap}")
                assert len(overlap) > 0, (
                    f"query text: {search_text}, \ntext: {result_text} \n overlap: {overlap} \n word freq a: {word_freq_a} \n word freq b: {word_freq_b}\n result: {r}"
                )

    @pytest.mark.tags(CaseLabel.L1)
    @pytest.mark.parametrize("nq", [2])
    @pytest.mark.parametrize("empty_percent", [0])
    @pytest.mark.parametrize("enable_partition_key", [True])
    @pytest.mark.parametrize("enable_inverted_index", [True])
    @pytest.mark.parametrize("index_type", ["SPARSE_INVERTED_INDEX"])
    @pytest.mark.parametrize("expr", [None])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_full_text_search_with_range_search(
        self,
        tokenizer,
        expr,
        enable_inverted_index,
        enable_partition_key,
        empty_percent,
        index_type,
        nq,
    ):
        """
        target: test full text search
        method: 1. enable full text search and insert data with varchar
                2. range search with text
                3. verify the result
        expected: full text search successfully and result is correct
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=enable_partition_key,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                enable_match=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        if tokenizer == "jieba":
            language = "zh"
            fake = fake_zh
        else:
            language = "en"

        data = [
            {
                "id": i,
                "word": fake.word().lower() if random.random() >= empty_percent else "",
                "sentence": fake.sentence().lower()
                if random.random() >= empty_percent
                else "",
                "paragraph": fake.paragraph().lower()
                if random.random() >= empty_percent
                else "",
                "text": fake.text().lower() if random.random() >= empty_percent else "",
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        texts = df["text"].to_list()
        word_freq = cf.analyze_documents(texts, language=language)
        tokens = list(word_freq.keys())
        if len(tokens) == 0:
            log.info("empty tokens, add a dummy token")
            tokens = ["dummy"]
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": index_type,
                "metric_type": "BM25",
                "params": {
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                },
            },
        )
        if enable_inverted_index:
            collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        limit = 1000
        search_data = [fake.text().lower() + random.choice(tokens) for _ in range(nq)]
        log.info(f"search data: {search_data}")
        # get distance with search data
        res_list, _ = collection_w.search(
            data=search_data,
            anns_field="text_sparse_emb",
            param={},
            limit=limit,  # get a wider range of search result
            output_fields=["id", "text"],
        )

        distance_list = []
        for i in range(nq):
            res = res_list[i]
            for j in range(len(res)):
                r = res[j]
                distance = r.distance
                distance_list.append(distance)
        distance_list = sorted(distance_list)
        # get the range of distance 30% ~70%
        low = distance_list[int(len(distance_list) * 0.3)]
        high = distance_list[int(len(distance_list) * 0.7)]

        res_list, _ = collection_w.search(
            data=search_data,
            anns_field="text_sparse_emb",
            param={"params": {"radius": low, "range_filter": high}},
            limit=limit,
            output_fields=["id", "text"],
        )
        # verify correctness
        for i in range(nq):
            log.info(f"res: {len(res_list[i])}")
            assert len(res_list[i]) < limit  # less than limit, because the range is set
            res = res_list[i]
            for j in range(len(res)):
                r = res[j]
                tmp_distance = r.distance
                assert low <= tmp_distance <= high

    @pytest.mark.tags(CaseLabel.L1)
    @pytest.mark.parametrize("nq", [1])
    @pytest.mark.parametrize("empty_percent", [0])
    @pytest.mark.parametrize("enable_partition_key", [True])
    @pytest.mark.parametrize("enable_inverted_index", [True])
    @pytest.mark.parametrize("index_type", ["SPARSE_INVERTED_INDEX"])
    @pytest.mark.parametrize("expr", [None])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_full_text_search_with_search_iterator(
        self,
        tokenizer,
        expr,
        enable_inverted_index,
        enable_partition_key,
        empty_percent,
        index_type,
        nq,
    ):
        """
        target: test full text search
        method: 1. enable full text search and insert data with varchar
                2. iterator search with text
                3. verify the result
        expected: full text search successfully and result is correct
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=enable_partition_key,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                enable_match=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        if tokenizer == "jieba":
            language = "zh"
            fake = fake_zh
        else:
            language = "en"

        data = [
            {
                "id": i,
                "word": fake.word().lower() if random.random() >= empty_percent else "",
                "sentence": fake.sentence().lower()
                if random.random() >= empty_percent
                else "",
                "paragraph": fake.paragraph().lower()
                if random.random() >= empty_percent
                else "",
                "text": fake.text().lower() if random.random() >= empty_percent else "",
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        texts = df["text"].to_list()
        word_freq = cf.analyze_documents(texts, language=language)
        tokens = list(word_freq.keys())
        if len(tokens) == 0:
            log.info("empty tokens, add a dummy token")
            tokens = ["dummy"]
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": index_type,
                "metric_type": "BM25",
                "params": {
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                },
            },
        )
        if enable_inverted_index:
            collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        search_data = [
            fake.text().lower() + " " + random.choice(tokens) for _ in range(nq)
        ]
        log.info(f"search data: {search_data}")
        # get distance with search data
        batch_size = 100
        limit = batch_size * 10
        iterator, _ = collection_w.search_iterator(
            data=search_data,
            anns_field="text_sparse_emb",
            batch_size=100,
            param={
                "metric_type": "BM25",
            },
            output_fields=["id", "text"],
            limit=limit,
        )
        iter_result = []
        while True:
            result = iterator.next()
            if not result:
                iterator.close()
                break
            else:
                iter_result.append(len(result))
        for r in iter_result[:-1]:
            assert r == batch_size


class TestSearchWithFullTextSearchNegative(TestcaseBase):
    """
    ******************************************************************
      The following cases are used to test search for full text search negative
    ******************************************************************
    """

    @pytest.mark.tags(CaseLabel.L2)
    @pytest.mark.parametrize("empty_percent", [0])
    @pytest.mark.parametrize("enable_partition_key", [True])
    @pytest.mark.parametrize("enable_inverted_index", [True])
    @pytest.mark.parametrize("index_type", ["SPARSE_INVERTED_INDEX"])
    @pytest.mark.parametrize("invalid_search_data", ["empty_text"])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    @pytest.mark.xfail(reason="issue: https://github.com/milvus-io/milvus/issues/37022")
    def test_search_for_full_text_search_with_empty_string_search_data(
        self,
        tokenizer,
        enable_inverted_index,
        enable_partition_key,
        empty_percent,
        index_type,
        invalid_search_data,
    ):
        """
        target: test full text search
        method: 1. enable full text search and insert data with varchar
                2. search with empty text
                3. verify the result
        expected: full text search successfully but result is empty
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=enable_partition_key,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        if tokenizer == "jieba":
            fake = fake_zh

        data = [
            {
                "id": i,
                "word": fake.word().lower() if random.random() >= empty_percent else "",
                "sentence": fake.sentence().lower()
                if random.random() >= empty_percent
                else "",
                "paragraph": fake.paragraph().lower()
                if random.random() >= empty_percent
                else "",
                "text": fake.text().lower() if random.random() >= empty_percent else "",
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": index_type,
                "metric_type": "BM25",
                "params": {
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                },
            },
        )
        if enable_inverted_index:
            collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        nq = 2
        limit = 100
        search_data = ["" for _ in range(nq)]
        log.info(f"search data: {search_data}")
        res, _ = collection_w.search(
            data=search_data,
            anns_field="text_sparse_emb",
            param={},
            limit=limit,
            output_fields=["id", "text"],
        )
        assert len(res) == nq
        for r in res:
            assert len(r) == 0

    @pytest.mark.tags(CaseLabel.L1)
    @pytest.mark.parametrize("empty_percent", [0])
    @pytest.mark.parametrize("enable_partition_key", [True])
    @pytest.mark.parametrize("enable_inverted_index", [True])
    @pytest.mark.parametrize("index_type", ["SPARSE_INVERTED_INDEX", "SPARSE_WAND"])
    @pytest.mark.parametrize("invalid_search_data", ["sparse_vector", "dense_vector"])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    def test_search_for_full_text_search_with_invalid_search_data(
        self,
        tokenizer,
        enable_inverted_index,
        enable_partition_key,
        empty_percent,
        index_type,
        invalid_search_data,
    ):
        """
        target: test full text search
        method: 1. enable full text search and insert data with varchar
                2. search with sparse vector or dense vector
                3. verify the result
        expected: full text search failed and return error
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=enable_partition_key,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        fake = fake_en
        if tokenizer == "jieba":
            language = "zh"
            fake = fake_zh
        else:
            language = "en"

        data = [
            {
                "id": i,
                "word": fake.word().lower() if random.random() >= empty_percent else "",
                "sentence": fake.sentence().lower()
                if random.random() >= empty_percent
                else "",
                "paragraph": fake.paragraph().lower()
                if random.random() >= empty_percent
                else "",
                "text": fake.text().lower() if random.random() >= empty_percent else "",
                "emb": [random.random() for _ in range(dim)],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        texts = df["text"].to_list()
        word_freq = cf.analyze_documents(texts, language=language)
        tokens = list(word_freq.keys())
        if len(tokens) == 0:
            log.info("empty tokens, add a dummy token")
            tokens = ["dummy"]
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.create_index(
            "emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": index_type,
                "metric_type": "BM25",
                "params": {
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                },
            },
        )
        if enable_inverted_index:
            collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        nq = 2
        limit = 100
        if invalid_search_data == "sparse_vector":
            search_data = cf.gen_vectors(
                nb=nq, dim=1000, vector_data_type=DataType.SPARSE_FLOAT_VECTOR
            )
        else:
            search_data = cf.gen_vectors(
                nb=nq, dim=1000, vector_data_type=DataType.FLOAT_VECTOR
            )
        log.info(f"search data: {search_data}")
        error = {
            ct.err_code: 65535,
            ct.err_msg: "please provide varchar/text for BM25 Function based search",
        }
        collection_w.search(
            data=search_data,
            anns_field="text_sparse_emb",
            param={},
            limit=limit,
            output_fields=["id", "text"],
            check_task=CheckTasks.err_res,
            check_items=error,
        )


# @pytest.mark.skip("skip")
class TestHybridSearchWithFullTextSearch(TestcaseBase):
    """
    ******************************************************************
      The following cases are used to test hybrid search with full text search
    ******************************************************************
    """

    @pytest.mark.tags(CaseLabel.L0)
    @pytest.mark.parametrize("empty_percent", [0])
    @pytest.mark.parametrize("enable_partition_key", [True])
    @pytest.mark.parametrize("enable_inverted_index", [True])
    @pytest.mark.parametrize("enable_group_by_field", [True, False])
    @pytest.mark.parametrize("index_type", ["SPARSE_INVERTED_INDEX"])
    @pytest.mark.parametrize("tokenizer", ["standard"])
    @pytest.mark.parametrize("inverted_index_algo", ct.inverted_index_algo)
    def test_hybrid_search_with_full_text_search(
        self,
        tokenizer,
        enable_inverted_index,
        enable_partition_key,
        empty_percent,
        index_type,
        inverted_index_algo,
        enable_group_by_field,
    ):
        """
        target: test full text search
        method: 1. enable full text search and insert data with varchar
                2. hybrid search with text, spase vector and dense vector
                3. verify the result
        expected: hybrid search successfully and result is correct
        """
        analyzer_params = {
            "tokenizer": tokenizer,
        }
        dim = 128
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(
                name="language",
                dtype=DataType.VARCHAR,
                max_length=16,
            ),
            FieldSchema(
                name="word",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
                is_partition_key=enable_partition_key,
            ),
            FieldSchema(
                name="sentence",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="paragraph",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
                enable_analyzer=True,
                enable_match=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(name="dense_emb", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="neural_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
            FieldSchema(name="text_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(fields=fields, description="test collection")
        bm25_function = Function(
            name="text_bm25_emb",
            function_type=FunctionType.BM25,
            input_field_names=["text"],
            output_field_names=["text_sparse_emb"],
            params={},
        )
        schema.add_function(bm25_function)
        data_size = 5000
        collection_w = self.init_collection_wrap(
            name=cf.gen_unique_str(prefix), schema=schema
        )
        language_list = ["en", "zh", "de", "jp", "unknown"]
        fake = fake_en
        data = [
            {
                "id": i,
                "language": random.choice(language_list),
                "word": fake.word().lower() if random.random() >= empty_percent else "",
                "sentence": fake.sentence().lower()
                if random.random() >= empty_percent
                else "",
                "paragraph": fake.paragraph().lower()
                if random.random() >= empty_percent
                else "",
                "text": fake.text().lower() if random.random() >= empty_percent else "",
                "dense_emb": [random.random() for _ in range(dim)],
                "neural_sparse_emb": cf.gen_vectors(
                    nb=1, dim=1000, vector_data_type=DataType.SPARSE_FLOAT_VECTOR
                )[0],
            }
            for i in range(data_size)
        ]
        df = pd.DataFrame(data)
        log.info(f"dataframe\n{df}")
        batch_size = 5000
        for i in range(0, len(df), batch_size):
            collection_w.insert(
                data[i : i + batch_size]
                if i + batch_size < len(df)
                else data[i : len(df)]
            )
        collection_w.create_index(
            "dense_emb",
            {
                "index_type": "HNSW",
                "metric_type": "L2",
                "params": {"M": 16, "efConstruction": 500},
            },
        )
        collection_w.create_index(
            "neural_sparse_emb",
            {"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "IP"},
        )
        collection_w.create_index(
            "text_sparse_emb",
            {
                "index_type": index_type,
                "metric_type": "BM25",
                "params": {
                    "bm25_k1": 1.5,
                    "bm25_b": 0.75,
                    "inverted_index_algo": inverted_index_algo,
                },
            },
        )
        if enable_inverted_index:
            collection_w.create_index("text", {"index_type": "INVERTED"})
        collection_w.load()
        nq = 2
        limit = 100
        bm25_search = AnnSearchRequest(
            data=[fake.text().lower() for _ in range(nq)],
            anns_field="text_sparse_emb",
            param={},
            limit=limit,
        )
        dense_search = AnnSearchRequest(
            data=[[random.random() for _ in range(dim)] for _ in range(nq)],
            anns_field="dense_emb",
            param={},
            limit=limit,
        )
        sparse_search = AnnSearchRequest(
            data=cf.gen_vectors(
                nb=nq, dim=dim, vector_data_type=DataType.SPARSE_FLOAT_VECTOR
            ),
            anns_field="neural_sparse_emb",
            param={},
            limit=limit,
        )
        # hybrid search
        res_list, _ = collection_w.hybrid_search(
            reqs=[bm25_search, dense_search, sparse_search],
            rerank=WeightedRanker(0.5, 0.5, 0.5),
            limit=limit,
            output_fields=["id", "text", "language"],
            group_by_field="language" if enable_group_by_field else None,
        )
        assert len(res_list) == nq
        # check the result correctness
        for i in range(nq):
            log.info(f"res length: {len(res_list[i])}")
            if enable_group_by_field:
                assert len(res_list[i]) == len(language_list)
            else:
                assert len(res_list[i]) == limit


class TestFullTextSearchMultiAnalyzer(TestcaseBase):
    """
    Comprehensive tests for multi_analyzer_params (multi-analyzer BM25) functionality in Milvus.
    Covers schema creation, data insertion, indexing, searching, alias/default/fallback, edge cases, and more.
    """

    @pytest.mark.tags(CaseLabel.L0)
    def test_create_collection_with_multi_analyzer(self):
        """
        target: test create collection with multi_analyzer_params
        method: create collection with multi_analyzer_params
        expected: create collection successfully
        """
        # Define multi_analyzer_params
        multi_analyzer_params = {
            "by_field": "language",
            "analyzers": {
                "en": {"type": "english"},
                "zh": {"type": "chinese"},
                "default": {"tokenizer": "icu"},
            },
            "alias": {"chinese": "zh", "eng": "en"},
        }
        # Define fields
        fields = [
            FieldSchema(name="doc_id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="language", dtype=DataType.VARCHAR, max_length=16),
            FieldSchema(
                name="article_content",
                dtype=DataType.VARCHAR,
                max_length=1024,
                enable_analyzer=True,
                multi_analyzer_params=multi_analyzer_params,
            ),
            FieldSchema(name="bm25_sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(
            fields=fields, description="Multi-analyzer BM25 test collection"
        )
        bm25_func = Function(
            name="bm25",
            function_type=FunctionType.BM25,
            input_field_names=["article_content"],
            output_field_names=["bm25_sparse_vector"],
        )
        schema.add_function(bm25_func)
        c_name = cf.gen_unique_str(prefix)
        collection_w = self.init_collection_wrap(name=c_name, schema=schema)
        res, _ = collection_w.describe()
        assert len(res["functions"]) == 1
        assert res["fields"][2]["name"] == "article_content"
        assert "multi_analyzer_params" in res["fields"][2]["params"]
        assert (
            json.loads(res["fields"][2]["params"]["multi_analyzer_params"])
            == multi_analyzer_params
        )

    @pytest.mark.tags(CaseLabel.L0)
    def test_insert_and_search_with_multi_analyzer(self):
        """
        target: test insert and search with multi_analyzer
        method: create collection, insert multilingual data, create index, search with analyzers
        expected: insert and search works, correct analyzer is used
        """
        multi_analyzer_params = {
            "by_field": "language",
            "analyzers": {
                "en": {"type": "english"},
                "zh": {"type": "chinese"},
                "default": {"tokenizer": "standard"},
            },
            "alias": {"chinese": "zh", "eng": "en"},
        }
        fields = [
            FieldSchema(name="doc_id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="language", dtype=DataType.VARCHAR, max_length=16),
            FieldSchema(
                name="article_content",
                dtype=DataType.VARCHAR,
                max_length=1024,
                enable_analyzer=True,
                multi_analyzer_params=multi_analyzer_params,
            ),
            FieldSchema(name="bm25_sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(
            fields=fields, description="Multi-analyzer BM25 test collection"
        )
        bm25_func = Function(
            name="bm25",
            function_type=FunctionType.BM25,
            input_field_names=["article_content"],
            output_field_names=["bm25_sparse_vector"],
        )
        schema.add_function(bm25_func)
        c_name = cf.gen_unique_str(prefix)
        collection_w = self.init_collection_wrap(name=c_name, schema=schema)
        # Prepare multilingual data
        language_samples = {
            "en": ["The quick brown fox.", "Machine learning is fun."],
            "zh": ["自然语言处理很重要。", "人工智能改变世界。"],
            "fr": ["L'intelligence artificielle.", "Traitement du langage naturel."],
            "unknown": ["Some random text for default analyzer."],
        }
        data = []
        idx = 0
        for lang, samples in language_samples.items():
            for s in samples:
                data.append({"doc_id": idx, "language": lang, "article_content": s})
                idx += 1
        collection_w.insert(data)
        fake_map = {
            "en": fake_en,
            "zh": fake_zh,
            "de": fake_de,
            "jp": fake_jp,
            "unknown": fake_en,
        }
        add_data = []
        for doc_id in range(idx, 3000):
            lang = random.choice(["en", "zh", "de", "jp", "unknown"])
            content = fake_map[lang].sentence()
            add_data.append(
                {"doc_id": doc_id, "language": lang, "article_content": content}
            )
        collection_w.insert(add_data)
        collection_w.create_index(
            "bm25_sparse_vector",
            {"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "BM25"},
        )
        collection_w.load()
        # Search with different analyzers
        analyzer_tests = [
            {"language": "en", "query": "machine learning", "analyzer_name": "en"},
            {"language": "zh", "query": "自然语言处理", "analyzer_name": "zh"},
            {
                "language": "fr",
                "query": "intelligence artificielle",
                "analyzer_name": "default",
            },
            {"language": "unknown", "query": "random text", "analyzer_name": "default"},
        ]
        for test in analyzer_tests:
            search_params = {
                "metric_type": "BM25",
                "analyzer_name": test["analyzer_name"],
            }
            results, _ = collection_w.search(
                data=[test["query"]],
                anns_field="bm25_sparse_vector",
                param=search_params,
                output_fields=["doc_id", "language", "article_content"],
                limit=5,
            )
            assert len(results) == 1
            assert len(results[0]) > 0
            log.info(
                f"Query '{test['query']}' with analyzer '{test['analyzer_name']}' returned {len(results[0])} results"
            )

    @pytest.mark.tags(CaseLabel.L0)
    def test_multi_analyzer_fallback(self):
        """
        target: test fallback to default analyzer
        method: insert data with languages not in analyzers, search without analyzer_name
        expected: fallback to default analyzer
        """
        multi_analyzer_params = {
            "by_field": "language",
            "analyzers": {
                "en": {"type": "english"},
                "zh": {"type": "chinese"},
                "default": {"tokenizer": "standard"},
            },
        }
        fields = [
            FieldSchema(name="doc_id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="language", dtype=DataType.VARCHAR, max_length=16),
            FieldSchema(
                name="article_content",
                dtype=DataType.VARCHAR,
                max_length=1024,
                enable_analyzer=True,
                multi_analyzer_params=multi_analyzer_params,
            ),
            FieldSchema(name="bm25_sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(
            fields=fields, description="Multi-analyzer fallback test"
        )
        bm25_func = Function(
            name="bm25",
            function_type=FunctionType.BM25,
            input_field_names=["article_content"],
            output_field_names=["bm25_sparse_vector"],
        )
        schema.add_function(bm25_func)
        c_name = cf.gen_unique_str(prefix)
        collection_w = self.init_collection_wrap(name=c_name, schema=schema)
        data = [
            {
                "doc_id": 1,
                "language": "en",
                "article_content": "English text for testing.",
            },
            {"doc_id": 2, "language": "zh", "article_content": "中文测试文本。"},
            {
                "doc_id": 3,
                "language": "fr",
                "article_content": "Texte français pour les tests.",
            },
            {
                "doc_id": 4,
                "language": "de",
                "article_content": "Deutscher Text zum Testen.",
            },
            {
                "doc_id": 5,
                "language": "unknown",
                "article_content": "Text in unknown language.",
            },
        ]
        collection_w.insert(data)
        collection_w.create_index(
            "bm25_sparse_vector",
            {"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "BM25"},
        )
        collection_w.load()
        fallback_tests = [
            {"language": "fr", "query": "texte français"},
            {"language": "de", "query": "deutscher text"},
            {"language": "unknown", "query": "unknown language"},
        ]
        for test in fallback_tests:
            search_params = {"metric_type": "BM25"}
            results, _ = collection_w.search(
                data=[test["query"]],
                anns_field="bm25_sparse_vector",
                param=search_params,
                output_fields=["doc_id", "language", "article_content"],
                limit=5,
            )
            assert len(results) == 1
            assert len(results[0]) > 0

    @pytest.mark.tags(CaseLabel.L0)
    def test_multi_analyzer_alias(self):
        """
        target: test alias for multi analyzer
        method: insert data with languages in alias
        expected: analyzer should be resolved correctly
        """
        stop_words = ["a", "an", "the", "of", "to", " "]
        multi_analyzer_params = {
            "by_field": "language",
            "analyzers": {
                "en": {
                    "tokenizer": "standard",
                    "filter": [
                        {
                            "type": "stop",  # Specifies 'stop' as the filter type
                            "stop_words": stop_words,  # Customizes stop words for this filter type
                        }
                    ],
                },
                "zh": {
                    "tokenizer": "jieba",
                    "filter": [
                        {
                            "type": "stop",  # Specifies 'stop' as the filter type
                            "stop_words": stop_words,  # Customizes stop words for this filter type
                        }
                    ],
                },
                "default": {"tokenizer": "icu"},
            },
            "alias": {"chinese": "zh", "eng": "en"},
        }
        fields = [
            FieldSchema(name="doc_id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="language", dtype=DataType.VARCHAR, max_length=16),
            FieldSchema(
                name="article_content",
                dtype=DataType.VARCHAR,
                max_length=8192,
                enable_analyzer=True,
                multi_analyzer_params=multi_analyzer_params,
            ),
            FieldSchema(name="bm25_sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(
            fields=fields, description="Multi-analyzer fallback test"
        )
        bm25_func = Function(
            name="bm25",
            function_type=FunctionType.BM25,
            input_field_names=["article_content"],
            output_field_names=["bm25_sparse_vector"],
        )
        schema.add_function(bm25_func)
        c_name = cf.gen_unique_str(prefix)
        collection_w = self.init_collection_wrap(name=c_name, schema=schema)
        data = [
            {
                "doc_id": 1,
                "language": "en",
                "article_content": "English text for testing",
            },
            {
                "doc_id": 2,
                "language": "eng",
                "article_content": "English text for testing"
                + " ".join(stop_words * 5),
            },
            {"doc_id": 3, "language": "zh", "article_content": "中文测试文本 "},
            {
                "doc_id": 4,
                "language": "chinese",
                "article_content": "中文测试文本 " + " ".join(stop_words * 5),
            },
            {
                "doc_id": 5,
                "language": "fr",
                "article_content": "Texte français pour les tests.",
            },
            {
                "doc_id": 6,
                "language": "de",
                "article_content": "Deutscher Text zum Testen.",
            },
            {
                "doc_id": 7,
                "language": "unknown",
                "article_content": "Text in unknown language.",
            },
            {
                "doc_id": 8,
                "language": "default",
                "article_content": " ".join(stop_words * 5),
            },
        ]
        # " ." * 1000 will be removed in en and zh analyzer, but will be kept in icu analyzer
        # if chinese and eng are not go to the alias as expected, then doc is 8 will be returned
        collection_w.insert(data)
        collection_w.create_index(
            "bm25_sparse_vector",
            {"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "BM25"},
        )
        collection_w.load()
        alias_tests = [
            {
                "analyzer_name": "eng",
                "query": "English text for testing." + " ".join(stop_words * 10),
            },
            {
                "analyzer_name": "chinese",
                "query": "中文测试文本。" + " ".join(stop_words * 10),
            },
        ]

        for test in alias_tests:
            search_params = {
                "metric_type": "BM25",
                "analyzer_name": test["analyzer_name"],
            }
            results, _ = collection_w.search(
                data=[test["query"]],
                anns_field="bm25_sparse_vector",
                param=search_params,
                output_fields=["doc_id", "language", "article_content"],
                limit=10,
            )
            log.info(test)
            log.info(results)
            assert len(results) == 1
            assert len(results[0]) > 0
            if test["analyzer_name"] == "eng":
                # return id is 1,2
                assert results[0][0]["doc_id"] in [1, 2]
                assert results[0][1]["doc_id"] in [1, 2]
            elif test["analyzer_name"] == "chinese":
                # return id is 3,4
                assert results[0][0]["doc_id"] in [3, 4]
                assert results[0][1]["doc_id"] in [3, 4]

        alias_tests = [
            {"analyzer_name": "icu", "query": " ".join(stop_words * 10)},
            {"analyzer_name": "default", "query": " ".join(stop_words * 10)},
        ]
        for test in alias_tests:
            search_params = {
                "metric_type": "BM25",
                "analyzer_name": test["analyzer_name"],
            }
            results, _ = collection_w.search(
                data=[test["query"]],
                anns_field="bm25_sparse_vector",
                param=search_params,
                output_fields=["doc_id", "language", "article_content"],
                limit=10,
            )
            log.info(test)
            log.info(results)
            assert len(results) == 1
            assert len(results[0]) > 0
            for r in results[0]:
                assert r["doc_id"] not in [1, 2, 3, 4]

    @pytest.mark.tags(CaseLabel.L0)
    def test_multi_analyzer_correctness(self):
        """
        target: test multi_analyzer correctness
        method: create collection, insert and search using utility
        expected: utility workflow works as expected
        """
        from utils.util_fts import FTSMultiAnalyzerChecker

        self._connect()
        client = self.client
        c_name = cf.gen_unique_str(prefix)
        language_field = "language"
        text_field = "article_content"
        ft_checker = FTSMultiAnalyzerChecker(
            collection_name=c_name,
            language_field_name=language_field,
            text_field_name=text_field,
            client=client,
        )
        ft_checker.init_collection()
        language_list = ["en", "zh", "fr", "jp"]
        data = ft_checker.generate_test_data(num_rows=100, lang_list=language_list)
        original_data, tokenized_data = ft_checker.insert_data(data)
        original_data = pd.DataFrame(original_data)
        ft_checker.create_index()
        sample_data = random.sample(tokenized_data, 10)
        for item in sample_data:
            doc_id = item["doc_id"]
            tokenized_query = item[text_field]
            original_query = original_data.loc[
                original_data["doc_id"] == doc_id, text_field
            ].iloc[0]
            language = item[language_field]
            res, mock_res = ft_checker.search(
                original_query, tokenized_query, language, limit=5
            )
            res_set = set([r["doc_id"] for r in res[0]])
            mock_res_set = set([r["doc_id"] for r in mock_res[0]])
            res_diff = res_set - mock_res_set
            mock_res_diff = mock_res_set - res_set
            if res_diff or mock_res_diff:
                log.error(f"result diff: {res_diff}, {mock_res_diff}")
                assert False, (
                    f"result diff: {res_diff} in origin but not in mock, {mock_res_diff} in mock but not in origin"
                )


class TestFullTextSearchMultiAnalyzerInvalid(TestcaseBase):
    """
    Cases for invalid multi_analyzer_params, should raise exceptions.
    """

    @pytest.mark.tags(CaseLabel.L0)
    def test_missing_by_field(self):
        """
        target: test missing by_field in multi_analyzer_params
        method: create collection without by_field
        expected: collection creation should fail because of missing by_field
        """
        missing_by_field = {
            "analyzers": {
                "en": {"type": "english"},
                "default": {"tokenizer": "standard"},
            }
        }
        fields = [
            FieldSchema(name="doc_id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="language", dtype=DataType.VARCHAR, max_length=16),
            FieldSchema(
                name="article_content",
                dtype=DataType.VARCHAR,
                max_length=1024,
                enable_analyzer=True,
                multi_analyzer_params=missing_by_field,
            ),
            FieldSchema(name="bm25_sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(
            fields=fields, description="Invalid multi-analyzer test"
        )
        bm25_func = Function(
            name="bm25",
            function_type=FunctionType.BM25,
            input_field_names=["article_content"],
            output_field_names=["bm25_sparse_vector"],
        )
        schema.add_function(bm25_func)
        collection_name = cf.gen_unique_str(prefix)
        with pytest.raises(Exception):
            self.init_collection_wrap(name=collection_name, schema=schema)

    @pytest.mark.tags(CaseLabel.L0)
    def test_by_field_not_exist(self):
        """
        target: test by_field not exist in multi_analyzer_params
        method: create collection with by_field not exist
        expected: collection creation should fail because of by_field not exist
        """
        missing_by_field = {
            "by_field": "not_exist",
            "analyzers": {
                "en": {"type": "english"},
                "default": {"tokenizer": "standard"},
            },
        }
        fields = [
            FieldSchema(name="doc_id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="language", dtype=DataType.VARCHAR, max_length=16),
            FieldSchema(
                name="article_content",
                dtype=DataType.VARCHAR,
                max_length=1024,
                enable_analyzer=True,
                multi_analyzer_params=missing_by_field,
            ),
            FieldSchema(name="bm25_sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(
            fields=fields, description="Invalid multi-analyzer test"
        )
        bm25_func = Function(
            name="bm25",
            function_type=FunctionType.BM25,
            input_field_names=["article_content"],
            output_field_names=["bm25_sparse_vector"],
        )
        schema.add_function(bm25_func)
        c_name = cf.gen_unique_str(prefix)
        with pytest.raises(Exception):
            self.init_collection_wrap(name=c_name, schema=schema)

    @pytest.mark.tags(CaseLabel.L0)
    def test_by_field_is_nullable(self):
        """
        target: test by_field is nullable in multi_analyzer_params
        method: create collection with by_field enable nullable
        expected: collection creation should success because by_field can be nullable
        """
        multi_analyzer_params = {
            "by_field": "language",
            "analyzers": {
                "en": {"type": "english"},
                "default": {"tokenizer": "standard"},
            },
        }
        fields = [
            FieldSchema(name="doc_id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="language", dtype=DataType.VARCHAR, max_length=16, nullable=True),
            FieldSchema(
                name="article_content",
                dtype=DataType.VARCHAR,
                max_length=1024,
                enable_analyzer=True,
                multi_analyzer_params=multi_analyzer_params,
            ),
            FieldSchema(name="bm25_sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(
            fields=fields, description="Invalid multi-analyzer test"
        )
        bm25_func = Function(
            name="bm25",
            function_type=FunctionType.BM25,
            input_field_names=["article_content"],
            output_field_names=["bm25_sparse_vector"],
        )
        schema.add_function(bm25_func)
        c_name = cf.gen_unique_str(prefix)
        collection_w = self.init_collection_wrap(name=c_name, schema=schema)

        data = [
            {
                "doc_id": 1,
                "language": "en",
                "article_content": "English text for testing.",
            },
            {"doc_id": 2, "language": "zh", "article_content": "中文测试文本。"},
            {
                "doc_id": 3,
                "language": "fr",
                "article_content": "Texte français pour les tests.",
            },
            {
                "doc_id": 4,
                "language": "de",
                "article_content": "Deutscher Text zum Testen.",
            },
            {
                "doc_id": 5,
                "language": "unknown",
                "article_content": "Text in unknown language.",
            },
            {"doc_id": 6, "language": None, "article_content": "nullable test"},
            {"doc_id": 7, "language": None, "article_content": "nullable test"},
        ]
        collection_w.insert(data)
        collection_w.create_index(
            "bm25_sparse_vector",
            {"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "BM25"},
        )
        collection_w.load()
        query_tests = [
            {"analyzer_name": "", "query": "texte français"},
            {"analyzer_name": "de", "query": "deutscher text"},
            {"analyzer_name": "unknown", "query": "unknown language"},
            {"analyzer_name": None, "query": "nullable language"},
        ]
        for test in query_tests:
            search_params = {
                "metric_type": "BM25",
                "analyzer_name": test["analyzer_name"],
            }
            results, _ = collection_w.search(
                data=[test["query"]],
                anns_field="bm25_sparse_vector",
                param=search_params,
                output_fields=["doc_id", "language", "article_content"],
                limit=5,
            )
            assert len(results) == 1
            assert len(results[0]) > 0

    @pytest.mark.tags(CaseLabel.L0)
    def test_text_field_is_nullable(self):
        """
        target: test text not exist in multi_analyzer_params
        method: create collection with by_field not exist
        expected: collection creation should fail because text field is nullable
        """
        multi_analyzer_params = {
            "by_field": "language",
            "analyzers": {
                "en": {"type": "english"},
                "default": {"tokenizer": "standard"},
            },
        }
        fields = [
            FieldSchema(name="doc_id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="language", dtype=DataType.VARCHAR, max_length=16),
            FieldSchema(
                name="article_content",
                dtype=DataType.VARCHAR,
                max_length=1024,
                enable_analyzer=True,
                multi_analyzer_params=multi_analyzer_params,
                nullable=True,
            ),
            FieldSchema(name="bm25_sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(
            fields=fields, description="Invalid multi-analyzer test"
        )
        bm25_func = Function(
            name="bm25",
            function_type=FunctionType.BM25,
            input_field_names=["article_content"],
            output_field_names=["bm25_sparse_vector"],
        )
        schema.add_function(bm25_func)
        c_name = cf.gen_unique_str(prefix)
        error = {
            ct.err_code: 65535,
            ct.err_msg: "function input field cannot be nullable",
        }
        self.init_collection_wrap(
            name=c_name, schema=schema, check_task=CheckTasks.err_res, check_items=error
        )

    @pytest.mark.tags(CaseLabel.L0)
    def test_missing_default_analyzer(self):
        """
        target: test missing default analyzer in multi_analyzer_params
        method: create collection without default analyzer
        expected: collection creation should fail because of no default analyzer
        """
        missing_default = {
            "by_field": "language",
            "analyzers": {"en": {"type": "english"}, "zh": {"type": "chinese"}},
        }
        fields = [
            FieldSchema(name="doc_id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="language", dtype=DataType.VARCHAR, max_length=16),
            FieldSchema(
                name="article_content",
                dtype=DataType.VARCHAR,
                max_length=1024,
                enable_analyzer=True,
                multi_analyzer_params=missing_default,
            ),
            FieldSchema(name="bm25_sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(
            fields=fields, description="Invalid multi-analyzer test"
        )
        bm25_func = Function(
            name="bm25",
            function_type=FunctionType.BM25,
            input_field_names=["article_content"],
            output_field_names=["bm25_sparse_vector"],
        )
        schema.add_function(bm25_func)
        collection_name = cf.gen_unique_str(prefix)
        with pytest.raises(Exception):
            self.init_collection_wrap(name=collection_name, schema=schema)

    @pytest.mark.tags(CaseLabel.L0)
    def test_alias_point_not_exist_analyzer(self):
        """
        target: test alias point to nonexist analyzer
        method: create collection with alias pointing to not exist analyzer
        expected: collection creation should success because fallback to default analyzer
        """
        missing_default = {
            "by_field": "language",
            "analyzers": {
                "en": {"type": "english"},
                "zh": {"type": "chinese"},
                "default": {"type": "english"},
            },
            "alias": {"chinese": "zh", "eng": "en", "fr": "fr"},
        }
        fields = [
            FieldSchema(name="doc_id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="language", dtype=DataType.VARCHAR, max_length=16),
            FieldSchema(
                name="article_content",
                dtype=DataType.VARCHAR,
                max_length=1024,
                enable_analyzer=True,
                multi_analyzer_params=missing_default,
            ),
            FieldSchema(name="bm25_sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
        ]
        schema = CollectionSchema(
            fields=fields, description="Invalid multi-analyzer test"
        )
        bm25_func = Function(
            name="bm25",
            function_type=FunctionType.BM25,
            input_field_names=["article_content"],
            output_field_names=["bm25_sparse_vector"],
        )
        schema.add_function(bm25_func)
        c_name = cf.gen_unique_str(prefix)
        self.init_collection_wrap(name=c_name, schema=schema)
