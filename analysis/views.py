import pandas as pd
from django.shortcuts import render, redirect
from .forms import UploadCSVForm
from .models import FinancialData
import matplotlib.pyplot as plt
import io
import base64

def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_csv')  # 成功したら同じページにリダイレクト
    else:
        form = UploadCSVForm()

    return render(request, 'upload.html', {'form': form})





def analyze(request, pk):
    financial_data = FinancialData.objects.get(pk=pk)
    
    # ファイルのエンコーディングを指定してCSVファイルを読み込む
    try:
        df = pd.read_csv(financial_data.csv_file.path, encoding='utf-8')
    except UnicodeDecodeError:
        # 'utf-8'で読み込めなかった場合は、'shift_jis'を試す
        df = pd.read_csv(financial_data.csv_file.path, encoding='shift_jis')
    
    # 以下、元のコード
    df['日付'] = pd.to_datetime(df['日付'])
    df['月'] = df['日付'].dt.to_period('M')

    grouped = df.groupby(['月', '勘定科目'])['金額'].sum().unstack(fill_value=0)
    revenue = grouped.get('売上', 0)
    material_costs = grouped.get('材料費', 0)
    expenses = grouped.get('経費', 0)

    plt.figure(figsize=(10, 6))
    plt.plot(revenue.index.astype(str), revenue, label='売上')
    plt.plot(material_costs.index.astype(str), material_costs, label='材料費')
    plt.plot(expenses.index.astype(str), expenses, label='経費')
    plt.xlabel('月')
    plt.ylabel('金額')
    plt.title('月別の勘定科目ごとの金額推移')
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    graph = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'analysis.html', {'graph': graph})
