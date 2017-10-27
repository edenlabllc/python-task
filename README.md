# Sample service for GitHub

## Overview

Simple python webservice that returns the objects and manipuates the data found
here [https://api.github.com/search/repositories/](https://api.github.com/search/repositories/).


## Requirements

* Django==1.11.6
* djangorestframework==3.7.1
* requests==2.18.4

## Installation

Install using `pip`...
```bash
pip install -r requirements.txt
```
## Importing data
Before getting data from GitHub search API v3 Insert you OAUTH tocken key to
settings.GITHUB_OAUTH.
For getting data from GitHub search API v3 use custom `fetchgithub` command

```bash
python manage.py fetchgithub [--last, --all]

```

## Endpoints

**/repositories/**

should return the first 100 objects ordered by `stargazers_count`.
