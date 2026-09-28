"""Compatibility import and CLI. Implementation lives in research/."""
if __name__ == "__main__":
    import runpy
    runpy.run_module("research.strube_evaluator", run_name="__main__")
else:
    from research.strube_evaluator import *
    from research.strube_evaluator import _interval_class, _is_target_interval
