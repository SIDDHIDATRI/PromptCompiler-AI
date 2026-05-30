import json
import os
import time
from collections import defaultdict

# METRICS TRACKER

class MetricsTracker:

    def __init__(self):

        self.total_requests = 0

        self.success_count = 0

        self.failure_count = 0

        self.retry_count = 0

        self.total_latency = 0

        self.failure_types = defaultdict(int)

        self.history = []

    # START TIMER

    def start_timer(self):

        return time.time()

    # END TIMER

    def end_timer(self, start_time):

        latency = (
            time.time() - start_time
        ) * 1000

        self.total_latency += latency

        return round(latency, 2)

    # SUCCESS EVENT

    def record_success(
        self,
        prompt,
        latency
    ):

        self.total_requests += 1

        self.success_count += 1

        self.history.append({

            "prompt": prompt,

            "status": "success",

            "latency_ms": latency
        })

    # FAILURE EVENT

    def record_failure(
        self,
        prompt,
        failure_type,
        latency
    ):

        self.total_requests += 1

        self.failure_count += 1

        self.failure_types[
            failure_type
        ] += 1

        self.history.append({

            "prompt": prompt,

            "status": "failure",

            "failure_type":
                failure_type,

            "latency_ms":
                latency
        })

    # RETRY EVENT

    def record_retry(self):

        self.retry_count += 1

    # REPORT

    def generate_report(self):

        avg_latency = 0

        if self.total_requests > 0:

            avg_latency = (

                self.total_latency
                / self.total_requests

            )

        report = {

            "total_requests":
                self.total_requests,

            "success_count":
                self.success_count,

            "failure_count":
                self.failure_count,

            "success_rate":

                round(

                    (
                        self.success_count
                        /
                        max(
                            self.total_requests,
                            1
                        )
                    )
                    * 100,

                    2
                ),

            "retry_count":
                self.retry_count,

            "average_latency_ms":

                round(
                    avg_latency,
                    2
                ),

            "failure_types":

                dict(
                    self.failure_types
                ),

            "history":
                self.history
        }

        os.makedirs(
            "artifacts",
            exist_ok=True
        )

        with open(

            "artifacts/metrics.json",

            "w"

        ) as f:

            json.dump(
                report,
                f,
                indent=4
            )

        return report