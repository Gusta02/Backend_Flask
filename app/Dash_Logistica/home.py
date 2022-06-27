from flask import Blueprint, render_template, request
from ..controllers.controller_logistica import IntegracaoWms
import pandas as pd

wms = Blueprint('wms', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

def leadtime():
    tabela = IntegracaoWms.leadtime()
    estado = IntegracaoWms.Estados()

    medias = []

    for index, row in estado.iterrows():

        Estado = row['estado']

        media = tabela.query(f'Estado=="{Estado}"')
        media = media['Dias']
        media = media.mean()
        media = f'{media: .0f}'
        medias.append(media)

    Media = pd.DataFrame(medias, columns = ['Media'])
    df =pd.concat([estado, Media], axis=1)
    print(df)

    return df

@wms.route('/', methods=["POST"])
def filtro_tabela():
    leadtime_Estado = leadtime()
    
    return render_template('index.html')
