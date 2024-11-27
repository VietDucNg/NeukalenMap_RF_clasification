# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 11:16:36 2024

@author: Viet Nguyen
"""
#### NOTE!: the script used variable from ipynb kernel

# how many grountruth point each year?
data_dict['2020']['class'].value_counts().sort_index()
data_dict['2021']['class'].value_counts().sort_index()
data_dict['2022']['class'].value_counts().sort_index()

# how many training point each year?
np.unique(class_train_dict['2020'], return_counts=True)
np.unique(class_train_dict['2021'], return_counts=True)
np.unique(class_train_dict['2022'], return_counts=True)

# how many training point each year?
np.unique(class_test_dict['2020'], return_counts=True)
np.unique(class_test_dict['2021'], return_counts=True)
np.unique(class_test_dict['2022'], return_counts=True)

#### plot feature importance
sorted_idx = np.argsort(clf.feature_importances_)
fig = plt.figure(figsize=(8, 6))
plt.barh(range(len(sorted_idx)), clf.feature_importances_[sorted_idx], align='center')
plt.yticks(range(len(sorted_idx)),np.array(band_names)[sorted_idx])
plt.title(f'Feature Importance')





