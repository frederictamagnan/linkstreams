from pandas.io.parsers import read_csv
from delta_density import *
from data_extraction import *


def one_file_deltadensity_list(linkstream, communities, delta_list, output_path):
    columns = ['community_id']+delta_list
    row_list = []
    for i in range(0,len(communities)):
        print(i)
        com_link = community_linkstream(link_streams=linkstream,community=communities[i])
        density_list = delta_density_list(com_link,delta_list,tspan=max(linkstream.t))
        row_list.append([i]+density_list)
    df = pd.DataFrame(row_list,columns=columns)
    df.to_csv(output_path,index=False)
    print('============ Finished ============')

def one_file_deltadensity(linkstream, communities, delta_list, output_path):
    delta_column = []
    deltadensity_column = []
    community_id_column = []
    for i in range(0, len(communities)):
        print(i)
        com_link = community_linkstream(link_streams=linkstream, community=communities[i])
        deltadensity_column += delta_density_list(link_stream=com_link, delta_list=delta_list,
                                                tspan=max(data['linkstream'].t) + 1)
        delta_column += delta_list
        community_id_column += list(np.repeat(i, repeats=len(delta_list)))
    to_csv_df = pd.DataFrame(
        {'community_id': community_id_column, 'delta': delta_column, 'deltadensity': deltadensity_column})
    to_csv_df.to_csv(output_path, index=False)
    print('============ Finished ============')

data = get_input(link_streams_path='../data/board/linkstream.csv',communities_path='../data/board/communities.json')
delta_list = list(np.arange(3600,max(data['linkstream'].t),7200))
delta_list = [int(i) for i in delta_list]
print(delta_list)
one_file_deltadensity(linkstream=data['linkstream'],communities=data['community'],delta_list=delta_list, output_path='../data/delta_density_result/result.csv')
one_file_deltadensity_list(linkstream=data['linkstream'],communities=data['community'],delta_list=delta_list, output_path='../data/delta_density_result/result_for_clustering.csv')