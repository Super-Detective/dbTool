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

Example 1:
Database  #show all databases
Table -database=SARS-CoV-2
Select -database=SARS-CoV-2 -table=BCR -columns=batch_name,barcode,contig_id,cdr3 -conditions='contig_id like "%_2"' -limit=10 -save -filepath='save_patch.csv'
Insert -database=SARS-CoV-2 -table=BCR -filepath='./test.csv' -unique_column=bcr_id
Update -database=SARS-CoV-2 -table=BCR -filepath='test.csv' -unique_column=bcr_id
Count -database=SARS-CoV-2 -table=BCR -conditions='contig_id like "%_2"'

Description:
--database：target databse
--table：target table
--columns: select **column(s)** from table
--filepath: save or input filepath
--unique_column: target columns to update or insert

**Example 2:**
Database
#show all databases

#You can create the configuration file config.ini in **current path** to simplify the instructions:
nano /software/dbTool-main/config.ini
**like**:
      [DEFAULT]
      DATABASE = SARS-CoV-2
      TABLE = TCR
**then**, -database and -table can ignore：
Table
Select -columns=batch_name,barcode,contig_id,cdr3 -conditions='contig_id like "%_2"' -limit=10 -save -filepath='save_patch.csv'
Insert -filepath='./test.csv' -unique_column=bcr_id
Update -filepath='test.csv' -unique_column=bcr_id
Count -conditions='contig_id like "%_2"


