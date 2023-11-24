# Database-tool
connect database and operation（show database、table and select...)
Step 1:
download dbTool.zip
Step 2:
unzip dbTool.zip
Step 3:
cd /dbTool
vim config.py
update host、user、password...
Step 4:
conda activate yout_env
cd ..
pip install .

Successfully installed dbTool-0.1
Done!

Example:
Database
Table -database=SARS-CoV-2
Select -database=SARS-CoV-2 -table=information -columns=id,name
