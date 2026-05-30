import json

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


tracker = MetricsTracker()


def evaluate_dataset(path):

    with open(path) as f:

        prompts = json.load(f)

    for prompt in prompts:

        start = tracker.start_timer()

        try:

            intent = extract_intent(
                prompt
            )

            architecture = (
                design_architecture(
                    intent
                )
            )

            config = (
                generate_complete_schema(
                    architecture
                )
            )

            validation = (
                validate_config(
                    config
                )
            )

            if not validation["valid"]:

                tracker.record_retry()

                config = repair_config(
                    config,
                    validation
                )

            simulate_runtime(config)

            latency = tracker.end_timer(
                start
            )

            tracker.record_success(
                prompt,
                latency
            )

        except Exception as e:

            latency = tracker.end_timer(
                start
            )

            tracker.record_failure(

                prompt,

                str(type(e).__name__),

                latency
            )

    return tracker.generate_report()


if __name__ == "__main__":

    real_report = evaluate_dataset(
        "datasets/real_prompts.json"
    )

    edge_report = evaluate_dataset(
        "datasets/edge_cases.json"
    )

    print(real_report)
    print(edge_report)