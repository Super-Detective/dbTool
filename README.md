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
Select -database=SARS-CoV-2 -table=BCR -columns=batch_name,barcode,contig_id,cdr3 -conditions='contig_id like "%_2"' -limit=10 -save -filepath='save_patch.csv'
Insert -database=SARS-CoV-2 -table=BCR -filepath='./test.csv' -unique_column=bcr_id
Update -database=SARS-CoV-2 -table=BCR -filepath='test.csv' -unique_column=bcr_id
Count -database=SARS-CoV-2 -table=BCR -conditions='contig_id like "%_2"' -count

Description:
--database：target databse
--table：target table
--columns: select **column(s)** from table
--filepath: save or input filepath
--unique_column: target columns to update or insert
--count: count number of target condition
