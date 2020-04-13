# Deploy Cognite Function action

![Deploy Cognite Function](https://github.com/andeplane/deploy-function-python/workflows/Deploy%20Cognite%20Function/badge.svg)

This action deploys a Python function to Cognite Functions.

## Inputs

### `function_path`

Path to a directory containing your function. By using strategy.matrix, multiple functions can be used.

### `cdf_project`

**Required** The name of the project in CDF.

### `cdf_credentials`

**Required** API key that should deploy the function.

### `cdf_base_url`

Base url of your CDF project. Defaults to https://api.cognitedata.com.

## Outputs

### `functionId`

The ID of the function you created.

## Example usage

```yml
uses: andeplane/deploy-function-python
with:
  cdf_project: cognite
  cdf_credentials: ${{ secrete.COGNITE_CREDENTIALS }}
```

Or see `.github/workflows` for a functioning example
