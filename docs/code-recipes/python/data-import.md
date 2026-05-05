---
title: "Python 数据导入"
---

# Python 数据导入

## CSV

```python
import pandas as pd

# 标准导入
df = pd.read_csv("data/adqs.csv")

# 指定列类型
df = pd.read_csv("data/adqs.csv", dtype={
    "subject": str,
    "treatment": "category",
    "visit": "category",
    "aval": float,
    "base": float
})
```

## SAS (sas7bdat)

```python
# 方法1: pandas 自带
adqs = pd.read_sas("data/adqs.sas7bdat")

# 方法2: pyreadstat（保留标签和格式）
import pyreadstat
adqs, meta = pyreadstat.read_sas7bdat("data/adqs.sas7bdat")

# 查看变量标签
print(meta.column_labels)
```

## XPT

```python
adsl = pd.read_sas("data/adsl.xpt", format="xport")
adtte = pd.read_sas("data/adtte.xpt", format="xport")
```

## Excel

```python
# 指定 sheet
df = pd.read_excel("data/data.xlsx", sheet_name="ADQS")

# 查看所有 sheet 名称
xl = pd.ExcelFile("data/data.xlsx")
print(xl.sheet_names)
```

## 批量导入

```python
import glob

files = glob.glob("data/*.sas7bdat")
datasets = {
    f.split("/")[-1].replace(".sas7bdat", ""): pd.read_sas(f)
    for f in files
}

# 解包到变量
adsl = datasets["adsl"]
adqs = datasets["adqs"]
adtte = datasets["adtte"]
```

## CDISC 标准数据集导入

```python
import pandas as pd

datasets = {}
for name in ["adsl", "adqs", "adtte", "adlb", "adae"]:
    datasets[name] = pd.read_sas(f"data/{name}.xpt", format="xport")
    print(f"{name}: {datasets[name].shape}")
```
