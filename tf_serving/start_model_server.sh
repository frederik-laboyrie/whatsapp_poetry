docker run -it -p 9000:9000 --name tf-serve -v $(pwd)/serve/:/serve/ epigramai/model-server:light-1.5 --port=9000 --model_name=test --model_base_path=/serve/test