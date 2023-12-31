# Dashboard Builder Example: CMS Data for Long Island

Built with [dashboard-builder](https://github.com/hantswilliams/dashboard-builder)! 

If you want to quickly visit the deployed version, please go to [https://dashboard-builder-nyhospitals.appliedhealthinformatics.com/](https://dashboard-builder-nyhospitals.appliedhealthinformatics.com/) to see the version currently running on GCP Cloud Run. 


## To run locally:
1. Create an virtual environment, or just pip install into your working env:
```bash
pip install -r requirements.txt
```

2. Run the flask application locally by navigating into the root directory of this project and doing: 
```bash
python main.py
```

3. Go the development server on your local computer at `127.0.0.1:5000`

## Deployment with GCP Cloud Run
1. Create a new project in GCP, and enable the Cloud Run API.
2. Followed these instructions [here](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service) to deploy the application.
    - `gcloud run deploy`
    
