import pathlib

from run_sims import manifest


if __name__=="__main__":
    print("Retrieving Eradication and schema.json packaged with emod-malaria...")
    import emod_malaria.bootstrap as emod_malaria_bootstrap
    emod_malaria_bootstrap.setup(pathlib.Path(manifest.eradication_path).parent)
    print("...done.")