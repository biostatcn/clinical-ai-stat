---
title: "SAS 分析宏"
---

# SAS 分析宏

## Table 1 宏程序

```sas
%macro table1(data=, strata=, vars=, cat_vars=);
    
    * 对连续变量计算描述统计;
    %let cont_vars =;
    %let i = 1;
    %let var = %scan(&vars, &i);
    %do %while(&var ne );
        %if %sysfunc(indexw(%str(&cat_vars), %str(&var))) = 0 %then
            %let cont_vars = &cont_vars &var;
        %let i = %eval(&i + 1);
        %let var = %scan(&vars, &i);
    %end;
    
    * 连续变量;
    proc means data=&data n mean std median q1 q3 min max;
        class &strata;
        var &cont_vars;
    run;
    
    * 分类变量;
    proc freq data=&data;
        tables &strata * (&cat_vars) / chisq;
    run;
    
%mend table1;

* 使用示例;
* %table1(data=adsl, strata=treatment, 
*          vars=age bmi sex race prior_med, 
*          cat_vars=sex race prior_med);
```

## MMRM 分析宏

```sas
%macro run_mmrm(data=, out=, var=, subject=, treatment=, 
                 visit=, baseline=, cov_type=un);
    
    proc mixed data=&data method=reml;
        class &subject &treatment &visit;
        model &var = &treatment | &visit &baseline / ddfm=kr solution;
        repeated &visit / subject=&subject type=&cov_type;
        
        lsmeans &treatment*&visit / slice=&visit diff cl;
        
        ods output lsmeans=lsmeans
                   diffs=diffs;
    run;
    
    * 提取治疗效应;
    data &out;
        set diffs;
        where &treatment = 1;  * Placebo 为参考组;
        est = estimate;
        lower = estimate - 1.96 * stderr;
        upper = estimate + 1.96 * stderr;
        pval = probt;
        keep &visit estimate stderr lower upper probt;
    run;
    
%mend run_mmrm;

* 使用示例;
* %run_mmrm(data=adqs_adam, out=result_mmrm,
*            var=chg, subject=subject,
*            treatment=trt01pn, visit=avisitn,
*            baseline=base, cov_type=un);
```

## 生存分析宏

```sas
%macro surv_analysis(data=, time=, event=, group=);
    
    * KM 曲线;
    ods graphics on;
    proc lifetest data=&data plots=survival(atrisk=0 to 24 by 6);
        time &time * &event(0);
        strata &group;
    run;
    
    * Cox 回归;
    proc phreg data=&data;
        class &group;
        model &time * &event(0) = &group / risklimits;
        hazardratio &group;
        
        * 比例风险假设检验;
        assess ph / resample;
    run;
    
%mend surv_analysis;

* 使用示例;
* %surv_analysis(data=adtte, time=avalu, event=event, group=treatment);
```

## 森林图数据准备宏

```sas
%macro forest_prep(data=, time=, event=, subgroup=);
    
    * 获取所有亚组水平;
    proc sql;
        select distinct &subgroup into :levels separated by "|"
        from &data
        where &subgroup ne "";
    quit;
    
    * 循环每个亚组做 Cox;
    %let count = %sysfunc(countw(&levels, |));
    data forest_results;
        length subgroup $40 hr lower upper pval n 8;
        call missing(subgroup, hr, lower, upper, pval, n);
        output;
        stop;
    run;
    
    * 先做 Overall;
    proc phreg data=&data;
        model &time * &event(0) = treatment / risklimits;
        ods output ParameterEstimates=overall;
    run;
    
    data overall;
        set overall;
        subgroup = "Overall";
        hr = exp(estimate);
        lower = exp(hazardlower);
        upper = exp(hazardupper);
        keep subgroup hr lower upper probchisq;
    run;
    
    proc append base=forest_results data=overall; run;
    
    %do i = 1 %to &count;
        %let level = %scan(&levels, &i, |);
        
        proc phreg data=&data;
            where &subgroup = "&level";
            model &time * &event(0) = treatment / risklimits;
            ods output ParameterEstimates=sub;
        run;
        
        data sub;
            set sub;
            subgroup = "&level";
            hr = exp(estimate);
            lower = exp(hazardlower);
            upper = exp(hazardupper);
            keep subgroup hr lower upper probchisq;
        run;
        
        proc append base=forest_results data=sub; run;
    %end;
    
%mend forest_prep;

* 使用示例;
* %forest_prep(data=adtte, time=avalu, event=event, subgroup=region);
```
