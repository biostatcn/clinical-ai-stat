---
title: "SAS 数据清洗"
---

# SAS 数据清洗

## 变量重编码

```sas
data adqs;
    set adqs;
    
    * 创建年龄分组;
    length agegrp $8;
    if age < 45 then agegrp = "< 45";
    else if age < 65 then agegrp = "45-64";
    else agegrp = ">= 65";
    
    * 创建二值终点;
    length responder $12;
    if aval >= 30 then responder = "Responder";
    else responder = "Non-responder";
    
    * BMI 分类;
    length bmigrp $12;
    if bmi < 18.5 then bmigrp = "Underweight";
    else if bmi < 25 then bmigrp = "Normal";
    else if bmi < 30 then bmigrp = "Overweight";
    else bmigrp = "Obese";
run;
```

## 衍生变量

```sas
data adqs;
    set adqs;
    
    * 较基线变化;
    chg = aval - base;
    
    * 百分比变化;
    pchg = (aval - base) / base * 100;
    
    * 对数转换;
    log_aval = log(aval);
    
    * 访视编号;
    length visitnum 8;
    select(visit);
        when("Baseline") visitnum = 0;
        when("Week 4")   visitnum = 4;
        when("Week 8")   visitnum = 8;
        when("Week 12")  visitnum = 12;
        when("Week 24")  visitnum = 24;
        otherwise        visitnum = .;
    end;
    
    * 改善标记;
    length improved $3;
    if chg < 0 then improved = "Yes";
    else improved = "No";
run;
```

## 缺失值处理

```sas
* 查看缺失值;
proc means data=adqs nmiss n;
    var aval base chg;
run;

* 删除缺失;
data adqs_clean;
    set adqs;
    if missing(aval) then delete;
run;

* LOCF 填补（纵向数据）;
data adqs_locf;
    set adqs;
    by subject visitnum;
    retain last_aval;
    
    if first.subject then last_aval = .;
    
    if not missing(aval) then last_aval = aval;
    else aval = last_aval;
run;

* 用中位数填补;
proc stdize data=adqs out=adqs_imp method=median reponly;
    var aval;
run;
```

## 合并数据集

```sas
* 纵向 + 受试者基线;
proc sort data=adqs; by subject; run;
proc sort data=adsl; by subject; run;

data adqs_merged;
    merge adqs (in=a)
          adsl (in=b keep=subject age sex race bmi);
    by subject;
    if a;  * 保留所有分析记录;
run;
```

## 数组处理（批量变量操作）

```sas
* 批量计算多个指标变化;
data adlb;
    set adlb;
    
    array lab{5} alt ast alp ggt tbil;
    array chglab{5} chg_alt chg_ast chg_alp chg_ggt chg_tbil;
    array baselab{5} base_alt base_ast base_alp base_ggt base_tbil;
    
    do i = 1 to 5;
        if not missing(lab{i}) and not missing(baselab{i}) then
            chglab{i} = lab{i} - baselab{i};
    end;
    
    drop i;
run;
```

## 定义格式

```sas
* 创建自定义格式;
proc format;
    value trt_fmt
        1 = "Placebo"
        2 = "Low Dose"
        3 = "High Dose";
    
    value resp_fmt
        0 = "Non-responder"
        1 = "Responder";
    
    value $site_fmt
        "001" = "Site A"
        "002" = "Site B"
        "003" = "Site C";
run;

* 应用格式;
data adsl;
    set adsl;
    format treatment trt_fmt.;
    format response resp_fmt.;
run;
```

## ADaM 数据准备

```sas
data adqs_adam;
    set adqs;
    
    * 筛选分析人群;
    where ittfl = "Y";
    
    * 定义分析变量;
    aval = chg;
    base = base;
    trt01pn = treatment;
    trt01p = put(treatment, trt_fmt.);
    
    * 访视排序;
    avisitn = visitnum;
    
    * 按主题访视排序;
    proc sort; by subject avisitn; run;
run;
```
