function [Add_file,Add_array] = file_compare(result_filepath1,pre_filepath)
[result_OutDir,result_Outarray]=fileprocess1(result_filepath1);
[Pre_OutDir,Pre_Outarray]=fileprocess2(pre_filepath);
[Add_file,Add_array]=Change(result_OutDir,Pre_OutDir,result_Outarray,Pre_Outarray);
end
