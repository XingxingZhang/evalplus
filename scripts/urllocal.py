
import os, sys, fire

urlmap = {
    "https://msranlp.blob.core.windows.net/unilm/": "/mnt/msranlp/",
    "https://msranlpintern.blob.core.windows.net/xingxing/": "/mnt/xingxing_blob/",
}

def urllocal(url):
    for url_prefix, local_prefix in urlmap.items():
        if url.startswith(url_prefix):
            print(local_prefix + url[len(url_prefix):])
            return
    
    raise RuntimeError('url not matchded!!!')

if __name__ == "__main__":
    fire.Fire(urllocal)
