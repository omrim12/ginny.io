## genie.io - Local Development
![genie image](genie_logo.png)
### Pre-requisites:
- Set `KAGGLE_USERNAME` and `KAGGLE_KEY` environment variables with your [Kaggle](https://www.kaggle.com/) credentials
- Set `FOOD_API_ID`, `FOOD_API_SECRET`, `RECIPES_API_ID` and `RECIPES_API_SECRET`
  environment variables with your [Edamam API](https://www.edamam.com/) credentials
- Download [food-101](https://www.kaggle.com/datasets/kmader/food41) images datasets from kaggle using `mount_food_101.py` script
### Get started with genie running following commands:
- Create a virtualenv:
```bash
python -m venv venv && source venv/bin/activate
```
- install requirements:
```bash
pip install -r requirements.txt
```
*Note: app requires python version>=3.10*
- run genie in CLI mode:
```bash
python genie_driver.py --cli-mode
```
- run genie in REST API mode:
```bash
python genie_driver.py --api-mode
```
- train a new genie CNN model with specific number of food types:
```bash
python genie_driver.py --new-genie --num-types=<number of supported food types>
```