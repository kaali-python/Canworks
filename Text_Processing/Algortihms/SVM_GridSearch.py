#!/usr/bin/env python
#-*- coding: utf-8 -*-


from sklearn.linear_model import SGDClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
import numpy

class SVMWithGridSearch:
	"""
	
	"""
	def __init__(self, data, target):
		self.data = data
		self.target = target

	def __classifier(self):
		#count_vect = CountVectorizer()
		#X_train_counts = count_vect.fit_transform(self.data)
		#tfidf_transformer = TfidfTransformer()
		#X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
		
		pipeline = Pipeline([ ('vect', CountVectorizer()),
					('tfidf', TfidfTransformer()),
					('clf', SGDClassifier()),
					])

		# uncommenting more parameters will give better exploring power but will
		# increase processing time in a combinatorial way

		parameters = { 'vect__max_df': (0.5, 0.75, 1.0),
				#'vect__max_features': (None, 5000, 10000, 50000),
				'vect__ngram_range': [(1, 1), (1, 2)],  # unigrams or bigrams
				#'tfidf__use_idf': (True, False),
				#'tfidf__norm': ('l1', 'l2'),
				'clf__alpha': (0.00001, 0.000001),
				'clf__penalty': ('l2', 'elasticnet'),
				#'clf__n_iter': (10, 50, 80),
				}

		grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)
		grid_search.fit(self.data, self.target)

		return grid_search


	def predict(self, data_to_predict):
		#vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')
		#X_test = vectorizer.transform(data_to_predict)
		classifier = self.__classifier()
		
		#count_vect = CountVectorizer()
		#tfidf_transformer = TfidfTransformer()
		#X_new_counts = count_vect.transform(numpy.array(data_to_predict))
		#X_new_tfidf = tfidf_transformer.transform(X_new_counts)

		prediction = classifier.predict(data_to_predict)

		return zip(data_to_predict, prediction)