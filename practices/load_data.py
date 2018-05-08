import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from megaphone_tokenizer import datasets


datasets.megaphones.generate_data_files()
# (x_train, y_train), (x_test, y_test) = datasets.megaphones.load_data()
# print(x_train)