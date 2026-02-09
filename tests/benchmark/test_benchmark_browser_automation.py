import os
import unittest
import pytest
from mcpuniverse.tracer.collectors import FileCollector
from mcpuniverse.benchmark.runner import BenchmarkRunner
from mcpuniverse.benchmark.report import BenchmarkReport
from mcpuniverse.callbacks.handlers.vprint import get_vprint_callbacks
from tests.benchmark.benchmark_utils import get_config_path_with_agent_override, cleanup_temp_config


class TestBenchmarkRunner(unittest.IsolatedAsyncioTestCase):

    @pytest.mark.skip
    async def test(self):
        # Get agent type from environment
        agent_type = os.environ.get("BENCHMARK_AGENT_TYPE", None)
        
        # Get config path (with optional agent type override)
        config_path = get_config_path_with_agent_override("test/browser_automation.yaml", agent_type)
        
        try:
            trace_collector = FileCollector(log_file="log/browser_automation.log")
            benchmark = BenchmarkRunner(config_path)
            benchmark_results = await benchmark.run(trace_collector=trace_collector, callbacks=get_vprint_callbacks())
            report = BenchmarkReport(benchmark, trace_collector=trace_collector)
            report.dump()

            print('=' * 66)
            print('Evaluation Result')
            print('-' * 66)
            for task_name in benchmark_results[0].task_results.keys():
                print(task_name)
                print('-' * 66)
                eval_results = benchmark_results[0].task_results[task_name]['evaluation_results']
                for eval_result in eval_results:
                    print("func:", eval_result.config.func)
                    print("op:", eval_result.config.op)
                    print("op_args:", eval_result.config.op_args)
                    print("value:", eval_result.config.value)
                    print('Passed?:', "\033[32mTrue\033[0m" if eval_result.passed else "\033[31mFalse\033[0m")
                    print('-' * 66)
        finally:
            cleanup_temp_config(config_path, agent_type)


if __name__ == "__main__":
    unittest.main()
