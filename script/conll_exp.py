import os
exp_name = 1107
vw_path =  '../vowpal_wabbit/vowpalwabbit/vw'
data = {'danish':{'name':'danish_ddt','num_tags':54,'root':True,'num_words':19150},\
		'arabic':{'name':'arabic_PADT','num_tags':28,'root':False,'num_words':13682},\
		'chinese':{'name':'chinese_sinica','num_tags':83,'root':True,'num_words':40929},\
		'czech':{'name':'czech_pdt','num_tags':83,'root':False,'num_words':130451},\
		'dutch':{'name':'dutch_alpino','num_tags':26,'root':True,'num_words':29123},\
		'japanese':{'name':'japanese_verbmobil','num_tags':8,'root':True,'num_words':3274},\
		'portuguese':{'name':'portuguese_bosque','num_tags':56,'root':False,'num_words':29489},\
		'slovene':{'name':'slovene_sdt','num_tags':27,'root':False,'num_words':8089},\
		'swedish':{'name':'swedish_talbanken05','num_tags':64,'root':True,'num_words':20684},
		}


def convert_data_into_vw_format():
	for key in data:
		
def train_models():
	for key in data:
		conll_train_file =  '../data/conll/'+key+'/'+data[key]['name']+'_train.conll.vw'
		model_name = data[key]['name']+'.%s.model'%exp_name
		num_tags = data[key]['num_tags']
		log_file = 'log/' + data[key]['name']
		os.system('time '+vw_path +' -k -c -d '+conll_train_file+' --passes 3 --search_task dep_parser --search '+ num_tags\
				+' --search_alpha 1e-4 --search_rollout oracle --holdout_off -f ' + model_name + ' --search_history_length 3 --search_no_caching \
				-b 24 --root_label 1 --num_label '+ num_tags + ' 1>'+log_file+'.logout 2>log/'+ log_file+'.logerr')
def test_models():
	for key in data:
		if not os.path.isfile(data[key]['name']+'.1107.model'):
			print 'Cannot find ' + (data[key]['name']+'.1107.model')
			continue
		conll_test_file =  '../data/conll/'+key+'/'+data[key]['name']+'_test.conll.vw'
		model_name = data[key]['name']+'.%s.model'%exp_name
		pred_file =   '../data/conll/'+key+'/'+data[key]['name']+'_test.pred'
		tag_Map =  '../data/conll/'+key+'/' + key+'.tagMap'
		os.system('time '+vw_path + ' -t  -c  -i ' + model_name +' -d ' + conll_test_file + ' -p ' + pred_file + '--search_no_caching  --root_label 1 --num_label '+ str(data[key]['num_tags']))
		os.system('python parseTestResult.py '+conll_test_file +  ' ' + pred_file  + ' ' + tag_Map + '  > tmpOut')
		os.system('python ../script/evaluate.py tmpOut ' + conll_test_file)

