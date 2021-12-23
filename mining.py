# we are going to analyze the effect of the frequency of classes in a week on the students' grades
import pandas as pd


def get_avg(data):
    scales = ['a_count', 'ab_count', 'b_count',
              'bc_count', 'c_count', 'd_count', 'f_count']
    data['total'] = data[scales].sum(axis=1)

    for e in scales:
        data[e] = data[e] / data['total']

    return data


grade_distributions = pd.read_csv('data/grade_distributions.csv')
schedules = pd.read_csv('data/schedules.csv')
sections = pd.read_csv('data/sections.csv')

new_schedule = schedules.merge(
    sections[['course_offering_uuid', 'schedule_uuid']], how='left', left_on='uuid', right_on='schedule_uuid')
new_grade = grade_distributions[['course_offering_uuid', 'section_number', 'a_count', 'ab_count',
                                 'b_count', 'bc_count', 'c_count', 'd_count', 'f_count']]

s_g = new_schedule.merge(new_grade, how='left', on='course_offering_uuid')

s_g = s_g[~
          ((s_g['mon'] == False) &
           (s_g['tues'] == False) &
           (s_g['wed'] == False) &
           (s_g['thurs'] == False) &
           (s_g['fri'] == False) &
           (s_g['sat'] == False) &
           (s_g['sun'] == False)
           )].replace({True: 1, False: 0})

s_g['freq'] = s_g['mon'] + s_g['tues'] + s_g['wed'] + \
    s_g['thurs'] + s_g['fri'] + s_g['sat'] + s_g['sun']
s_g = get_avg(s_g)

print(s_g.groupby(by=s_g['freq']).agg({'a_count': 'mean',
                                       'ab_count': 'mean',
                                       'b_count': 'mean',
                                       'bc_count': 'mean',
                                       'c_count': 'mean',
                                       'd_count': 'mean',
                                       'f_count': 'mean',
                                       'uuid': 'count'}))
'''
       a_count  ab_count   b_count  bc_count   c_count   d_count   f_count    uuid
freq                                                                              
1     0.476028  0.179319  0.197520  0.061622  0.061042  0.015371  0.009098  328966
2     0.360717  0.215745  0.243265  0.088752  0.066912  0.016133  0.008476  261080
3     0.379568  0.301413  0.199774  0.053307  0.044437  0.011644  0.009859  130909
4     0.329151  0.254270  0.269451  0.060292  0.063305  0.014335  0.009197   29498
5     0.505153  0.158326  0.202138  0.048145  0.061640  0.014302  0.010295   19236
6     0.449564  0.315271  0.224005  0.008551  0.002422  0.000000  0.000187   42435
7     0.237719  0.280955  0.467364  0.012645  0.000000  0.000000  0.001317      95
'''
