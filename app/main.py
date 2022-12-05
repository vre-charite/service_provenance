# Copyright 2022 Indoc Research
# 
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
# 
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import ConfigClass, SRV_NAMESPACE
from .api_registry import api_registry
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.elasticsearch import ElasticsearchInstrumentor

def create_app():
    '''
    create app function
    '''
    app = FastAPI(
        title="Service Provenance",
        description="Service Provenance",
        docs_url="/v1/api-doc",
        version=ConfigClass.version
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API registry
    # v1
    api_registry(app)
    if ConfigClass.opentelemetry_enabled:
        instrument_app(app)

    return app

def instrument_app(app) -> None:
    """Instrument the application with OpenTelemetry tracing."""

    tracer_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: SRV_NAMESPACE}))
    trace.set_tracer_provider(tracer_provider)

    jaeger_exporter = JaegerExporter(
        agent_host_name='127.0.0.1', agent_port=6831
    )

    tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()
    ElasticsearchInstrumentor().instrument()
