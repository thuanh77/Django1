from .models import Result
import pandas as pd


def db_process(y_test, y_pred_rgr, y_pred_bst, y_pred_rnn):

    df = pd.DataFrame({
        'Real_result': y_test.reshape(-1),
        'PL_regression': y_pred_rgr.reshape(-1),
        'Gradient_Boosting': y_pred_bst,
        'RNN': y_pred_rnn
    })

    Result.objects.all().delete()
    db.session.commit()

    results = [Result(
        Real_result=row['Real_result'],
        PL_regression=row['PL_regression'],
        Gradient_boosting=row['Gradient_Boosting'],
        RNN=row['RNN']
    ) for index, row in df.iterrows()]

    db.session.bulk_save_objects(results)
    db.session.commit()