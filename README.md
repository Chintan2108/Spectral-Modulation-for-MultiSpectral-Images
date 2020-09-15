# Spectral-Modulation-for-MultiSpectral-Images
Modulation based classification for multi-spectral satellite images
* Supervised classification is performed for multispectral images
* Different classes are identified by a modulation function 
* Modulation function is defined as peak signal recorded in each band of the image
  * If 4 bands: b1, b2, b3, b4 and pattern as (130, 100, 70, 76) then modulation pattern is defined as: 222220 based on (130>100, 130>100, 130>70, 130>76, 100>76, 100>70, 70<76).
  * '2' represents preceeding band value is greater
  * '1' represents succeeding band value is greater
  * '0' represents both band values are equal
* If there are 4 bands in an image, then the resulting image array is of dimension rows x cols x 4. This way, each pixel is a vector of 4 values.
* The above modulation is applied on each pixel vector and underlying classes are identified
* Finetuning is done to merge redundant classes
