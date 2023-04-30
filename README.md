# Get started

## Clone the repo
```
git clone git@github.com:NaregB/phishing-detector-model.git
```

## Create venv and install requirements
[Link to docs](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

# Usage

## Find best fit
Test various parameter combinations and visualize the result in `notebook.ipynb`

## Train the model
After finding the params, train and save the final model
```
python scripts/train_and_save_model.py
```

> **Note**
>
> it will be saved in `model/PhishingModel.joblib` file

# Deployment

## Prepare lambda
Copy created `PhishingModel.joblib` file to `aws/lambda` folder, or run the command
```
cp model/PhishingModel.joblib aws/lambda/
```

## Create zip archive
Run the command to create an archive
```
make zip
```

## Upload to AWS lambda
Go to lambda in AWS management console and upload the created zip

> **Note**
>
> If you create AWS lambda for the first time, layers should be uploaded too. Just create a zip archive of each layer and upload to AWS lambda layers
>
> [Creating and sharing Lambda layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
