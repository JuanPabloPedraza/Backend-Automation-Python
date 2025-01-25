#!/bin/bash
pytest tests/ --alluredir=reports/
allure serve reports/
