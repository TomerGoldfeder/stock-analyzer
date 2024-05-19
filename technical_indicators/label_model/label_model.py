from snorkel.labeling.model import MajorityLabelVoter, LabelModel
from snorkel.labeling import PandasLFApplier

from technical_indicators.label_model.labeling_functions import get_labeling_functions, apply_lfs



def train_predict_label_model_1(applied_labeling_functions):
    label_model = MajorityLabelVoter(cardinality=2)
    labeling_functions_names = [x.name for x in get_labeling_functions()]
    only_labeling_functions = applied_labeling_functions[labeling_functions_names].values
    applied_labeling_functions['preds'] = label_model.predict(only_labeling_functions)

    means = []
    for i in range(only_labeling_functions.shape[0]):
        buys = []
        sells = []
        for j in range(only_labeling_functions.shape[1]):
            if only_labeling_functions[i][j] == 1:
                buys.append(j)
            elif only_labeling_functions[i][j] == 0:
                sells.append(j)
        if applied_labeling_functions.iloc[i]['preds'] == 1:
            means.append(len(buys) / (len(buys) + len(sells)))
        else:
            means.append(len(sells) / (len(buys) + len(sells)))
    applied_labeling_functions['preds_proba'] = means # label_model.predict_proba(only_labeling_functions).max(axis=1)
    return applied_labeling_functions

def train_predict_label_model(applied_labeling_functions):
    labeling_funcs = get_labeling_functions()
    labeling_functions_names = [x.name for x in labeling_funcs]

    label_model = LabelModel(cardinality=2)
    preprocessor = PandasLFApplier(labeling_funcs)
    L_train = preprocessor.apply(applied_labeling_functions)

    label_model.fit(L_train)

    only_labeling_functions = applied_labeling_functions[labeling_functions_names].values
    applied_labeling_functions['preds'] = label_model.predict(only_labeling_functions)
    applied_labeling_functions['preds_proba'] = label_model.predict_proba(only_labeling_functions).max(axis=1)
    applied_labeling_functions = applied_labeling_functions[applied_labeling_functions['preds_proba'] > 0.5]
    print(applied_labeling_functions['preds_proba'].describe())
    return applied_labeling_functions
