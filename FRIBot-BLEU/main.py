from BLEUService import BLEUService

bleu_service = BLEUService('./network_4_1.h5', './data/final_dataset_backend_dictionaries', 127, 512, './data/final_dataset_vars')
bleu_service.calculate_bleu_score()