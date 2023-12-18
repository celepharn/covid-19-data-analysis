<h1>🐛 Data analysis of conditions contributing to COVID-19 deaths</h1>
<p> Here I analyse the conditions contributing to COVID-19 deaths using <a href="https://catalog.data.gov/dataset/conditions-contributing-to-deaths-involving-coronavirus-disease-2019-covid-19-by-age-group">data provided by the US government</a>.</p

## Try it yourself
<p>To use this follow the instructions</p>

```
git clone https://github.com/celepharn/covid-19-data-analysis.git
cd covid-19-data-analysis
python3 covid-analysis.py
```
<p>and finally inspect the covid.sqlite file with db browser or with the cli sqlite utility, as an example</p>

```
SELECT COUNT(*) 
FROM Member
WHERE cond_id = '61';
```
<p>this says how many times did hypertension disease contributed to COVID-19 deaths, or also</p>

```
SELECT COUNT(*) 
FROM Member
WHERE cond_id = '61'
AND age_id = 1';
```
<p>this would extract the times hypertension diseas contributed to COVID-19 deaths when the person was also in the age group 1, which is 0-24 years old.</p>
<p>I am working on data visualization which hopefully will be done in the next weeks because of holidays.</p>
