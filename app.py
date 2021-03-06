import pandas as pd
import pyarrow
from flask import Flask, render_template, jsonify
import pickle
import lightgbm as lgb
from lightgbm import LGBMClassifier
import os


app= Flask(__name__)

model_lgb = open('LightGBMModel.pkl','rb')
lgbm = pickle.load(model_lgb)

data_client = pd.read_feather('data_client')
data_client.sort_values(by=['SK_ID_CURR'], inplace = True)

#Préparation du df qui va servir à la prédiction
features = ['SK_ID_CURR','NEW_EXT_MEAN',
 'EXT_SOURCE_3',
 'OWN_CAR_AGE',
 'CODE_GENDER',
 'AMT_ANNUITY',
 'EXT_SOURCE_2',
 'PAYMENT_RATE',
 'EXT_SOURCE_1',
 'AMT_CREDIT',
 'ANNUITY_INCOME_PERC',
 'DAYS_EMPLOYED',
 'NEW_APP_EXT_SOURCES_PROD',
 'AMT_GOODS_PRICE',
 'NAME_EDUCATION_TYPE_HIGHER_EDUCATION',
 'DAYS_BIRTH',
 'NEW_GOODS_CREDIT',
 'AMT_INCOME_TOTAL',
 'PREV_CHANNEL_TYPE_CREDIT_AND_CASH_OFFICES_MEAN',
 'PREV_NAME_YIELD_GROUP_LOW_ACTION_MEAN',
 'DAYS_EMPLOYED_PERC',
 'INS_DBD_STD',
 'APPROVED_AMT_ANNUITY_MEDIAN',
 'CLOSED_DAYS_CREDIT_ENDDATE_STD',
 'OCCUPATION_TYPE_CORE_STAFF',
 'INS_AMT_PAYMENT_MEDIAN',
 'INS_DPD_MEAN',
 'AMT_REQ_CREDIT_BUREAU_QRT',
 'INS_DBD_SUM',
 'FLAG_OWN_CAR',
 'INS_AMT_PAYMENT_MIN',
 'BUREAU_DAYS_CREDIT_UPDATE_MAX',
 'REGION_POPULATION_RELATIVE',
 'BUREAU_AMT_CREDIT_SUM_MEAN',
 'DAYS_REGISTRATION',
 'DAYS_ID_PUBLISH',
 'APPROVED_AMT_ANNUITY_STD',
 'BUREAU_AMT_CREDIT_SUM_MEDIAN',
 'PREV_CHANNEL_TYPE_REGIONAL_LOCAL_MEAN',
 'INS_NUM_INSTALMENT_NUMBER_MAX',
 'NEW_C_GP',
 'INS_DBD_MEAN',
 'NAME_EDUCATION_TYPE_SECONDARY_SECONDARY_SPECIAL',
 'INS_AMT_PAYMENT_MAX',
 'INS_PAYMENT_DIFF_SUM',
 'INS_DPD_STD',
 'TOTALAREA_MODE',
 'NONLIVINGAPARTMENTS_AVG',
 'INCOME_PER_PERSON',
 'INS_DBD_MEDIAN',
 'APPROVED_HOUR_APPR_PROCESS_START_STD',
 'BUREAU_AMT_CREDIT_SUM_STD',
 'ACTIVE_DAYS_CREDIT_ENDDATE_MIN',
 'NAME_FAMILY_STATUS_MARRIED',
 'PREV_DAYS_LAST_DUE_MAX',
 'PREV_NAME_GOODS_CATEGORY_MOBILE_MEAN',
 'APPROVED_RATE_DOWN_PAYMENT_STD',
 'APPROVED_DAYS_DECISION_MEDIAN',
 'ACTIVE_DAYS_CREDIT_MAX',
 'DEF_30_CNT_SOCIAL_CIRCLE',
 'CLOSED_DAYS_CREDIT_MAX',
 'PREV_APP_CREDIT_PERC_STD',
 'PREV_HOUR_APPR_PROCESS_START_MEAN',
 'INS_DAYS_ENTRY_PAYMENT_MAX',
 'POS_MONTHS_BALANCE_MAX',
 'BUREAU_DAYS_CREDIT_UPDATE_MEDIAN',
 'NAME_INCOME_TYPE_WORKING',
 'CC_AMT_PAYMENT_TOTAL_CURRENT_MEAN',
 'CLOSED_DAYS_CREDIT_UPDATE_MAX',
 'POS_NAME_CONTRACT_STATUS_ACTIVE_MEAN',
 'INS_PAYMENT_DIFF_MAX',
 'CLOSED_DAYS_CREDIT_ENDDATE_MIN',
 'INS_NUM_INSTALMENT_NUMBER_SUM',
 'PREV_NAME_TYPE_SUITE_UNACCOMPANIED_MEAN',
 'PREV_DAYS_DECISION_MAX',
 'INS_DAYS_INSTALMENT_STD',
 'INS_AMT_INSTALMENT_MEDIAN',
 'PREV_DAYS_LAST_DUE_1ST_VERSION_MEAN',
 'PREV_DAYS_FIRST_DUE_MEDIAN',
 'INS_AMT_INSTALMENT_MEAN',
 'PREV_PRODUCT_COMBINATION_CASH_X_SELL_LOW_MEAN',
 'BUREAU_AMT_CREDIT_MAX_OVERDUE_STD',
 'POS_CNT_INSTALMENT_STD',
 'AMT_REQ_CREDIT_BUREAU_YEAR',
 'REFUSED_DAYS_DECISION_STD',
 'PREV_DAYS_LAST_DUE_1ST_VERSION_MAX',
 'INS_PAYMENT_DIFF_MEAN',
 'INCOME_PER_PERSON_PERC_PAYMENT_RATE',
 'INS_AMT_PAYMENT_STD',
 'DAYS_LAST_PHONE_CHANGE',
 'LIVINGAREA_MEDI',
 'INS_DBD_MAX',
 'PREV_NAME_PAYMENT_TYPE_CASH_THROUGH_THE_BANK_MEAN',
 'POS_CNT_INSTALMENT_FUTURE_STD',
 'PREV_APP_CREDIT_PERC_MEDIAN',
 'PREV_CNT_PAYMENT_MEAN',
 'PREV_CNT_PAYMENT_MEDIAN',
 'BUREAU_AMT_CREDIT_SUM_DEBT_MEDIAN',
 'POS_MONTHS_BALANCE_SIZE',
 'PREV_HOUR_APPR_PROCESS_START_MIN',
 'INS_AMT_INSTALMENT_MAX']
data_lgb = data_client[features]
data_lgb.set_index('SK_ID_CURR', inplace = True)

@app.route('/loan/<int:id_client>', methods = ['GET'])
def loan(id_client):
    id=id_client
    predict = lgbm.predict(data_lgb.loc[id].values.reshape(1,-1))
    
    output = {'prediction' : int(predict)}
    
    return jsonify(output)
    
if __name__== '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(debug = True)
