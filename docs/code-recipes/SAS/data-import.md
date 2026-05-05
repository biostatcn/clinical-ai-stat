---
title: "SAS 数据导入"
---

# SAS 数据导入

## CSV → SAS

```sas
proc import datafile="data/adqs.csv" out=adqs dbms=csv replace;
    guessingrows=10000;  * 防止变量截断;
run;

proc import datafile="data/adsl.csv" out=adsl dbms=csv replace;
run;
```

## SAS 数据集导入

```sas
libname indata "C:/rawdata";
data adqs;
    set indata.adqs;
run;
```

## XPT (CDISC) 导入

```sas
* 方法1: libname 直连;
libname xptin xport "data/adsl.xpt";
data adsl;
    set xptin.adsl;
run;

* 方法2: proc copy;
libname xptin xport "data/adtte.xpt";
libname out "data";
proc copy in=xptin out=out;
run;
```

## Excel 导入

```sas
proc import datafile="data/data.xlsx"
    out=adqs dbms=xlsx replace;
    sheet="ADQS";
run;
```

## 批量导入目录下所有 SAS 数据集

```sas
filename files pipe 'dir /b "C:\data\*.sas7bdat"';
data _null_;
    infile files truncover;
    input filename $200.;
    call execute(cats(
        'data ', compress(scan(filename, 1, '.')), '; ',
        '  set "C:\data\', filename, '"; ',
        'run;'
    ));
run;
```

## 导入时指定变量属性

```sas
data adqs;
    length subject $10 treatment $20 visit $10;
    set adqs;
    format aval 8.2 base 8.2;
    label 
        subject = "Subject ID"
        treatment = "Treatment Arm"
        aval = "Analysis Value"
        base = "Baseline Value";
run;
```
