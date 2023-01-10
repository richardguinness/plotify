#################### PACKAGE ACTIONS ###################

reinstall_package:
	@pip uninstall -y plotify-backend || :
	@pip install -e .

run_api:
	uvicorn api.fast:app --reload
