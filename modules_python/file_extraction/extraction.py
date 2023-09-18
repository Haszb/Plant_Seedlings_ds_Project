
def read_plant_datasets(
        path            : str, 
        reshape         : tuple     = [(160, 160), (300, 300)],
        return_as       : str       = 'X_y', 
        subset          : str       ='train_set', 
        channel_type    : str       = "RGB", 
        verbose         : any       = None, 
        limit           : any       = None,
        type_indexes    : list      = [1], 
        image_idexes    : any       = None,
        add_contrast    : bool      = False
        ):
    """
    ----------------------------------------------------------

    >>> Copyright : Iréné A. Essomba (c) 2023

    ----------------------------------------------------------


    - This python module is used for EXTRACT LOAD and TRANSFORM data 

    * path :  is a string value that represent the absolute patht where the data are located.
    * return_as : is a type of returning  --> (ditc or X_y) if you need more values used dict
    * subset : is a string value , default value : train_set 
    * verbose : is an integer or None value used to print the processes of data treatment
    * type_indexes : is a list value that specifies which directory do you want to process, 
    * image_indexes : is also a list that used to select the image to process
    * add_contrast : is a boolean valeur, used to add light intensity on the image
    * channel_type is string value. all values take into account are bellow : 

    * -------------------------------------------------------------------------------------

    >>> channel_type = ["RBG-HSV", "SIMPLE_GRAY", "RGB", "HIS-C", "HIS-EQ","HIS-ADAPT", 
            "HIS-DISK", "GAUSSIAN", "RGR2-HSV", "RGR2-LAB" ]

    * -------------------------------------------------------------------------------------

    >>> path = '/document/images'
    
    * In this directory you have for example 5 others diectories --> (dogs, cats, lions, births, wolf)
    
    >>> data_process = read_plant_datasets(path=path, return_as='dict', verbose=1, type_indexes=[0, 2, 3])
    >>> data_process = read_plant_datasets(path=path, return_as='dict', verbose=1, type_indexes=[0, 2, 3])

    * type_indexes=[0, 2, 3] means that you will just process --> (dogs, lions, births) directories
    * So imagine that each directory has 10K files if you do not want to process all you can fix image_indexes values as follow :

    >>> image_indexes = list(range(0, 10000, 2))
    >>> data_process = read_plant_datasets(path=path, return_as='dict', verbose=1, 
            type_indexes=[0, 2, 3], image_indexes=image_indexes, reshape=[(160, 160)])

    * when using "ditc" as return key the output is schemed as follow:

    >>> data_reshaping{
            "160x160 : "data = { 
                        'X' : X, 
                        'images' : true_imgs,
                        "target" : y, 
                        "feature_names" : feature_names, 
                        'subset' : subset, 
                        "channel_type" : channel_type, 
                        "number_of_images" : number_of_imgames,
                        "shape" : reshape,
                        "sobels" : sobels,
                        "rapport" : rapport,
                        "pixels" : pixels,
                        "width"  : widths,
                        "height" : heights,
                        "paths"  : paths

                    }   
        } 


    >>> X is the image (ELT)
    >>> images is the original images
    >>> target is the targets values
    >>> features names is (dogs, lions, births)
    >>> subset is train_set
    >>> channel_type is RBG (default value)
    >>> number_of_images the number of images per speces
    >>> shape is the windows shaping
    >>> sobels the number of RGBA contain in the original image
    >>> rapport is width / heigth
    >>> pixels is (with * height) / 1024
    >>> width and height are the dimension of each images

    * When using X_y as key
    The output is as follow  :

    output = (X, target)

    >>> X is the image (ELT)
    >>> target is the targets values
    """

    import os, sys
    import numpy as np
    import matplotlib.pyplot as plt
    import platform
    from   sklearn.preprocessing import LabelEncoder
    from modules_python.image_processing import preprocessing
    from alive_progress import alive_bar
    from time import sleep
    from modules_python.config import config

    # nettoyage de l'écran
    sys.stdout.write(
        config.clear.screen(pos=2) + config.cursorPos.to(x=0, y=0)
        )
    
    # obtenir tous les répertoires de path
    types = os.listdir(path)


    print(
        f"{config.fg.rbg(0,255,0)}{'-'*100}\
        \n{config.fg.rbg(255, 0, 255)}{config.init.bold} {len(types)} répertoires trouvés\
        \n{config.fg.rbg(0,255,0)}{'-'*100}{config.init.reset}"
        )
    
    for i in range(len(types)):
        print(
            config.init.bold + \
            config.fg.rbg(255, 255, 0) + \
            types[i] + config.init.reset
            )
    print(
        f'{config.fg.rbg(0,255,0)}{"-"*100}{config.init.reset}', '\n\n\n')

    # verification du système d'exploiation 
    system                      = platform.system()
    # en codage des données 
    feature_names               = types 
    # encoding feature names
    target                      = LabelEncoder().fit_transform(feature_names)
    # Chemin du répertoire contenant les images (remplacez "chemin_vers_votre_repertoire" par le chemin approprié)
    repertoire_images           = path
    if     reshape  : 
        data_reshaping          = {f"{xx[0]}x{xx[1]}" : None for xx in reshape}
    else            : 
        data_reshaping          = {f"{reshape}" : None}
        reshape                 = [None]

    number_of_imgames   = []
    
    # initialisation des la liste de stokage des images et des cibles associées 
    for shape in reshape:
        X, y, sobels            = [[], [], []]
        rapport, pixels         = [[], []]
        widths, heights         = [[],[]]
        true_imgs, _paths_      = [[],[]]   

        if verbose == 1: 
            print(
                f'{config.fg.rbg(0,255,0)}{"-"*100}\
                \n{config.init.bold + config.fg.rbg(255, 0,255)} dimension = {shape[0]}x{shape[1]} {config.init.reset}\n'
                )

        for i in type_indexes:
            typ = types[i]

            if verbose == 1: 
                print(
                    f'{config.fg.rbg(0,255,0)}{"-"*100}\
                    \n{config.init.bold + config.fg.rbg(255, 0,0)}{typ} <-----> index {i}{config.init.reset}'
                    )

            X_type, y_type, num_img, sob = [], [], [], []
            r_, pix             = [[], []]
            width, height       = [[],[]]
            true_img, _path_    = [[],[]]

            # nom du repertoire pour chaque espèces
            if   system in ["Windows"] : repertoire_images_esp = f"{repertoire_images}\\" + f"{typ}"
            elif system in ["Linux", "MacOS"] : repertoire_images_esp = f"{repertoire_images}/" + f"{typ}"
            else:
                white   = config.fg.rbg(255,255,255)
                red     = config.fg.rbg(255,0, 0)
                green   = config.fg.rbg(0,255,0)

                error = white + f"Le système {red}{system}{white} n'est pas pris en compte" + config.init.reset
                print(f"\n{error}\n") 
                break

            # Liste tous les fichiers d'images dans le répertoire
            images = [f for f in os.listdir(repertoire_images_esp) if f.endswith(('.jpg', '.png', '.jpeg'))]
            print(len(images))
            # nombre d'iamges dans le répertoire repertoire_images_esp
            size = len(images)

            # Parcourir la liste des fichiers d'images
            if    limit is None: pass 
            else: images = images[: limit]

            with alive_bar(len(images), title = types[i]) as NAME : 
                if image_idexes is None: image_idexes = list(range(size))

                try:
                    for j, image_filename in enumerate(images):
                        #if j in image_idexes:
                        # Construisez le chemin complet du fichier image
                        chemin_image = os.path.join(repertoire_images_esp, image_filename)

                        # storing the all_paths
                        if   system in ["Windows"] : _path_.append(f"{repertoire_images_esp}\\{image_filename}")
                        elif system in ["Linux", "MacOS"] : _path_.append(f"{repertoire_images_esp}/{image_filename}")
                        else: pass 

                        # Lisez l'image
                        image = plt.imread(chemin_image)
                        width.append(image.shape[1])
                        height.append(image.shape[0])
                        # calcul du nombre de pixels de l'image 
                        r, pixel = preprocessing.Size(image=image)

                        # conversion de rbga à rbg (channel = 4 ---> chennel = 3)
                        image_, sobel = preprocessing.image_processing(image=image.copy(), name=channel_type, reshape=shape, add_contrast=add_contrast)
                        _true_image_, sobel = preprocessing.image_processing(image=image.copy(), name='RBG', reshape=shape)
                        # Vous pouvez effectuer des opérations sur l'image ici, si nécessaire
                        #image = cv2.resize(src=image, dsize=reshape)
                        
                        X_type.append(image_)
                        true_img.append(_true_image_)
                        y_type.append(target[i])
                        num_img.append(1)
                        sob.append(sobel * 1.0)
                        r_.append(r)
                        pix.append(pixel)
                        #else: pass 

                        sleep(.001)
                        NAME()
                except IndexError:
                    print(f"Index {j} out of range")
                    break

                # stockage des données en fonction des features
                X.append(np.array(X_type))
                true_imgs.append(np.array(true_img))
                # cible 
                y.append(np.array(y_type))
                # number of images per categories
                number_of_imgames.append( sum(num_img) )
                # nombre d'image en rgba par catégories
                sobels.append(sum(sob))
                # rapport width / height par catégories
                rapport.append(r_)
                # pixels par images
                pixels.append(pix)
                # largeur 
                widths.append(width)
                # hauteur
                heights.append(height)
                # paths
                _paths_.append(_path_)

        if len(types) == 1 : 
            X = np.array( X_type, dtype="object" )
            true_imgs = np.array(true_img, dtype="object")
            y = np.array( y_type )
        else : 
            X = np.array(X, dtype="object")
            true_imgs = np.array(true_imgs, dtype="object")
            y = np.array(y, dtype=object)

        data = { 
            'X'             : X, 
            'images'        : true_imgs,
            "target"        : target, 
            "feature_names" : feature_names, 
            'subset'        : subset, 
            "channel_type"  : channel_type, 
            "number_of_images" : number_of_imgames,
            "shape"         : shape,
            "sobels"        : sobels,
            "rapport"       : rapport,
            "pixels"        : pixels,
            "width"         : widths,
            "height"        : heights,
            "paths"         : _paths_
        }

        if   return_as == "dict" : data_reshaping[f"{shape[0]}x{shape[1]}"] = data.copy()
        elif return_as == "X_y"  : data_reshaping[f"{shape[0]}x{shape[1]}"] = {"X" : data['images'], 'target' : data["target"]}
        else :
            error = config.fg.rbg(255,255,255) + f"return_as is not in {config.fg.rbg(0,255,0)}['X_y', 'dict']" + config.init.reset
            print( error )
    if verbose == 1:
        print(
            f"\n{config.fg.rbg(0,255,0)}{'-'*100}\
            \n{config.init.bold + config.fg.rbg(0,255,255)}Processus Extraction-Chargement-Transformation (ELT) terminé !!!!!\
            \n{config.fg.rbg(0,255,0)}{'-'*100}{config.init.reset}\n\n\n"
            )
   
    return data_reshaping