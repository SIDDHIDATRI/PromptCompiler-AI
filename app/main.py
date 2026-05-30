from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from app.pipeline.intent_extractor import (
    extract_intent
)

from app.pipeline.system_designer import (
    design_architecture
)

from app.pipeline.schema_generator import (
    generate_complete_schema
)

from app.pipeline.validator import (
    validate_config
)

from app.pipeline.repair_engine import (
    repair_config
)

from app.pipeline.runtime_simulator import (
    simulate_runtime
)

from app.pipeline.metrics_tracker import (
    MetricsTracker
)

# APP SETUP

app = FastAPI(
    title="Prompt Compiler AI",
    version="1.0.0"
)

metrics_tracker = MetricsTracker()


# REQUEST MODEL

class UserPrompt(BaseModel):

    prompt: str

# HEALTH CHECK

@app.get("/health")
def health():

    return {

        "status": "healthy",

        "service":
            "prompt-compiler-ai"
    }

# METRICS ENDPOINT

@app.get("/metrics")
def metrics():

    return metrics_tracker.generate_report()



# MAIN GENERATION ENDPOINT

@app.post("/generate")
def generate_app(user_input: UserPrompt):

    start_time = (
        metrics_tracker.start_timer()
    )

    try:

        # ==================================================
        # Stage 1
        # ==================================================

        intent = extract_intent(
            user_input.prompt
        )

        # ==================================================
        # Stage 2
        # ==================================================

        architecture = (
            design_architecture(
                intent
            )
        )

        # ==================================================
        # Stage 3
        # ==================================================

        config = (
            generate_complete_schema(
                architecture
            )
        )

        # ==================================================
        # Stage 4
        # ==================================================

        validation_result = (
            validate_config(
                config
            )
        )

        repair_performed = False

        # ==================================================
        # Stage 5
        # ==================================================

        if not validation_result["valid"]:

            repair_performed = True

            metrics_tracker.record_retry()

            config = repair_config(

                config,

                validation_result
            )

            validation_result = (

                validate_config(
                    config
                )

            )

        # ==================================================
        # Stage 6
        # ==================================================

        runtime_result = (
            simulate_runtime(
                config
            )
        )

        latency = (

            metrics_tracker.end_timer(
                start_time
            )

        )

        metrics_tracker.record_success(

            user_input.prompt,

            latency
        )

        return {

            "status":
                "success",

            "pipeline": {

                "intent_extraction":
                    "completed",

                "system_design":
                    "completed",

                "schema_generation":
                    "completed",

                "validation":
                    "completed",

                "repair":
                    repair_performed,

                "runtime":
                    "completed"
            },

            "intent":
                intent,

            "architecture":
                architecture,

            "validation":
                validation_result,

            "runtime":
                runtime_result,

            "final_config":
                config,

            "latency_ms":
                latency
        }

    except Exception as e:

        latency = (

            metrics_tracker.end_timer(
                start_time
            )

        )

        metrics_tracker.record_failure(

            user_input.prompt,

            type(e).__name__,

            latency
        )

        return JSONResponse(

            status_code=500,

            content={

                "status":
                    "failure",

                "error":
                    str(e),

                "error_type":
                    type(e).__name__
            }
        )