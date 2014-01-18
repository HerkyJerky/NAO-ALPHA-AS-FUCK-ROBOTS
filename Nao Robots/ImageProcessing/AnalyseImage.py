import Distance as distance
import cProfile
import pstats

class AnalyseImage:
    
    
    def __init__(self):
        pass
    
        # self.data = []    self.data was never used, so no need to create empty array
    
    def analyse(self, imageName):
        self.d = distance.Distance(imageName)
        return self.d.getData()
    
    
def test_case():
    an = AnalyseImage()
    #dat = [(boolean goalpost, double distance (in meter), double theta (in rad)), ......]
    dat = an.analyse('9jan03-3.png')
    print(dat)
    
if __name__ == "__main__":
    cProfile.run('test_case()', 'profile_results')
    
    profile_stats = pstats.Stats('profile_results')
    profile_stats.sort_stats('cumulative').print_stats(20)

'''
============================= Results before optimization: =============================

IMAGE:                 9jan03-1.png

ALGORITHM OUTPUT:    []

PROFILER OUTPUT:

Sat Jan 18 17:14:17 2014    profile_results

         769533 function calls (769532 primitive calls) in 3.740 seconds

   Ordered by: cumulative time
   List reduced from 129 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    3.740    3.740 <string>:1(<module>)
        1    0.000    0.000    3.740    3.740 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\AnalyseImage.py:16(test_case)
        1    0.000    0.000    3.740    3.740 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\AnalyseImage.py:11(analyse)
        1    0.000    0.000    3.740    3.740 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\Distance.py:12(__init__)
        1    1.002    1.002    3.307    3.307 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:51(startLumi)
        1    0.052    0.052    0.823    0.823 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:134(removeBackGround)
        1    0.771    0.771    0.771    0.771 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:296(onlyWhite)
        1    0.729    0.729    0.729    0.729 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:81(calculateGoalposts)
        1    0.348    0.348    0.407    0.407 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:24(getAverageLightIntensity)
    76800    0.321    0.000    0.370    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ColorSysCustom.py:43(rgb_to_hue)
    76800    0.190    0.000    0.190    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:304(acceptedLumi)
   107520    0.134    0.000    0.190    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ColorSysCustom.py:7(rgb_to_luminance)
   184320    0.062    0.000    0.062    0.000 {max}
   184326    0.042    0.000    0.042    0.000 {min}
    70217    0.031    0.000    0.031    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:318(acceptedYellow)
    68426    0.029    0.000    0.029    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:311(acceptedGreen)
        1    0.000    0.000    0.018    0.018 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\Distance.py:28(findLandmarks)
        1    0.000    0.000    0.008    0.008 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:10(__init__)
        1    0.006    0.006    0.006    0.006 {cv2.HoughLinesP}
        1    0.005    0.005    0.005    0.005 {cv2.Canny}

------------------------------------------------------------------

IMAGE:                 9jan03-2.png

ALGORITHM OUTPUT:    []

PROFILER OUTPUT:

Sat Jan 18 17:14:54 2014    profile_results

         763680 function calls (763679 primitive calls) in 3.862 seconds

   Ordered by: cumulative time
   List reduced from 129 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    3.862    3.862 <string>:1(<module>)
        1    0.000    0.000    3.862    3.862 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\AnalyseImage.py:16(test_case)
        1    0.000    0.000    3.862    3.862 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\AnalyseImage.py:11(analyse)
        1    0.000    0.000    3.862    3.862 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\Distance.py:12(__init__)
        1    1.011    1.011    3.430    3.430 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:51(startLumi)
        1    0.198    0.198    0.957    0.957 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:134(removeBackGround)
        1    0.758    0.758    0.758    0.758 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:296(onlyWhite)
        1    0.707    0.707    0.707    0.707 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:81(calculateGoalposts)
        1    0.355    0.355    0.416    0.416 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:24(getAverageLightIntensity)
    76800    0.324    0.000    0.372    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ColorSysCustom.py:43(rgb_to_hue)
   107520    0.137    0.000    0.193    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ColorSysCustom.py:7(rgb_to_luminance)
    76800    0.191    0.000    0.191    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:304(acceptedLumi)
   184320    0.062    0.000    0.062    0.000 {max}
   184326    0.042    0.000    0.042    0.000 {min}
    66832    0.029    0.000    0.029    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:318(acceptedYellow)
    66148    0.028    0.000    0.028    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:311(acceptedGreen)
        1    0.000    0.000    0.009    0.009 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:10(__init__)
        1    0.000    0.000    0.008    0.008 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\Distance.py:28(findLandmarks)
        1    0.005    0.005    0.005    0.005 {cv2.Canny}
        1    0.005    0.005    0.005    0.005 {cv2.imread}
        
------------------------------------------------------------------

IMAGE:                 9jan03-3.png

ALGORITHM OUTPUT:    [(True, 1.0460266561986848, 0.05061454830783556)]

PROFILER OUTPUT:

Sat Jan 18 17:15:48 2014    profile_results

         757088 function calls (757087 primitive calls) in 4.052 seconds

   Ordered by: cumulative time
   List reduced from 130 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    4.052    4.052 <string>:1(<module>)
        1    0.000    0.000    4.052    4.052 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\AnalyseImage.py:16(test_case)
        1    0.000    0.000    4.052    4.052 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\AnalyseImage.py:11(analyse)
        1    0.000    0.000    4.052    4.052 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\Distance.py:12(__init__)
        1    1.001    1.001    3.617    3.617 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:51(startLumi)
        1    0.263    0.263    1.031    1.031 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:134(removeBackGround)
        1    0.828    0.828    0.828    0.828 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:81(calculateGoalposts)
        1    0.767    0.767    0.767    0.767 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:296(onlyWhite)
        1    0.350    0.350    0.410    0.410 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:24(getAverageLightIntensity)
    76800    0.329    0.000    0.377    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ColorSysCustom.py:43(rgb_to_hue)
    76800    0.191    0.000    0.191    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:304(acceptedLumi)
   107520    0.136    0.000    0.191    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ColorSysCustom.py:7(rgb_to_luminance)
   184320    0.062    0.000    0.062    0.000 {max}
   184326    0.041    0.000    0.041    0.000 {min}
    70054    0.030    0.000    0.030    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:318(acceptedYellow)
    56182    0.024    0.000    0.024    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:311(acceptedGreen)
        1    0.000    0.000    0.016    0.016 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\Distance.py:28(findLandmarks)
        1    0.000    0.000    0.009    0.009 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:10(__init__)
        1    0.007    0.007    0.007    0.007 {cv2.HoughLinesP}
        1    0.005    0.005    0.005    0.005 {cv2.Canny}
        
------------------------------------------------------------------

IMAGE:                 9jan03-4.png

ALGORITHM OUTPUT:    [(False, 1.0927233979547699, -0.030368728984701332)]

PROFILER OUTPUT:

Sat Jan 18 17:16:31 2014    profile_results

         761985 function calls (761984 primitive calls) in 3.776 seconds

   Ordered by: cumulative time
   List reduced from 130 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    3.776    3.776 <string>:1(<module>)
        1    0.000    0.000    3.776    3.776 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\AnalyseImage.py:16(test_case)
        1    0.000    0.000    3.776    3.776 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\AnalyseImage.py:11(analyse)
        1    0.000    0.000    3.776    3.776 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\Distance.py:12(__init__)
        1    1.009    1.009    3.343    3.343 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:51(startLumi)
        1    0.131    0.131    0.899    0.899 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:134(removeBackGround)
        1    0.767    0.767    0.767    0.767 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:296(onlyWhite)
        1    0.688    0.688    0.688    0.688 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:81(calculateGoalposts)
        1    0.350    0.350    0.409    0.409 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:24(getAverageLightIntensity)
    76800    0.318    0.000    0.366    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ColorSysCustom.py:43(rgb_to_hue)
   107520    0.136    0.000    0.191    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ColorSysCustom.py:7(rgb_to_luminance)
    76800    0.189    0.000    0.189    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:304(acceptedLumi)
   184320    0.062    0.000    0.062    0.000 {max}
   184326    0.042    0.000    0.042    0.000 {min}
    65850    0.030    0.000    0.030    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:318(acceptedYellow)
    65337    0.028    0.000    0.028    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:311(acceptedGreen)
        1    0.000    0.000    0.015    0.015 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\Distance.py:28(findLandmarks)
        1    0.000    0.000    0.009    0.009 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:10(__init__)
        1    0.006    0.006    0.006    0.006 {cv2.HoughLinesP}
        1    0.005    0.005    0.005    0.005 {cv2.Canny}
        
------------------------------------------------------------------

IMAGE:                 9jan03-5.png

ALGORITHM OUTPUT:    []

PROFILER OUTPUT:

Sat Jan 18 17:17:15 2014    profile_results

         763765 function calls (763764 primitive calls) in 3.992 seconds

   Ordered by: cumulative time
   List reduced from 129 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    3.992    3.992 <string>:1(<module>)
        1    0.000    0.000    3.992    3.992 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\AnalyseImage.py:16(test_case)
        1    0.000    0.000    3.992    3.992 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\AnalyseImage.py:11(analyse)
        1    0.000    0.000    3.992    3.992 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\Distance.py:12(__init__)
        1    1.033    1.033    3.544    3.544 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:51(startLumi)
        1    0.192    0.192    0.996    0.996 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:134(removeBackGround)
        1    0.804    0.804    0.804    0.804 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:296(onlyWhite)
        1    0.765    0.765    0.765    0.765 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:81(calculateGoalposts)
        1    0.362    0.362    0.423    0.423 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:24(getAverageLightIntensity)
    76800    0.310    0.000    0.359    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ColorSysCustom.py:43(rgb_to_hue)
   107520    0.139    0.000    0.196    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ColorSysCustom.py:7(rgb_to_luminance)
    76800    0.195    0.000    0.195    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:304(acceptedLumi)
   184320    0.063    0.000    0.063    0.000 {max}
   184326    0.043    0.000    0.043    0.000 {min}
    67241    0.030    0.000    0.030    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:318(acceptedYellow)
    65712    0.029    0.000    0.029    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:311(acceptedGreen)
        1    0.000    0.000    0.017    0.017 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\Distance.py:28(findLandmarks)
        1    0.000    0.000    0.008    0.008 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:10(__init__)
        1    0.006    0.006    0.006    0.006 {cv2.HoughLinesP}
        1    0.006    0.006    0.006    0.006 {cv2.Canny}
        
------------------------------------------------------------------

IMAGE:                 9jan03-6.png

ALGORITHM OUTPUT:    []

PROFILER OUTPUT:

Sat Jan 18 17:17:58 2014    profile_results

         761283 function calls (761282 primitive calls) in 3.861 seconds

   Ordered by: cumulative time
   List reduced from 129 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    3.861    3.861 <string>:1(<module>)
        1    0.000    0.000    3.861    3.861 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\AnalyseImage.py:16(test_case)
        1    0.000    0.000    3.861    3.861 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\AnalyseImage.py:11(analyse)
        1    0.000    0.000    3.861    3.861 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\Distance.py:12(__init__)
        1    1.006    1.006    3.413    3.413 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:51(startLumi)
        1    0.204    0.204    0.956    0.956 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:134(removeBackGround)
        1    0.752    0.752    0.752    0.752 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:296(onlyWhite)
        1    0.697    0.697    0.697    0.697 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:81(calculateGoalposts)
        1    0.356    0.356    0.416    0.416 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:24(getAverageLightIntensity)
    76800    0.319    0.000    0.369    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ColorSysCustom.py:43(rgb_to_hue)
   107520    0.137    0.000    0.193    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ColorSysCustom.py:7(rgb_to_luminance)
    76800    0.191    0.000    0.191    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:304(acceptedLumi)
   184320    0.063    0.000    0.063    0.000 {max}
   184326    0.043    0.000    0.043    0.000 {min}
    65984    0.030    0.000    0.030    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:318(acceptedYellow)
    64487    0.028    0.000    0.028    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:311(acceptedGreen)
        1    0.000    0.000    0.018    0.018 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:10(__init__)
        1    0.000    0.000    0.014    0.014 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\Distance.py:28(findLandmarks)
        1    0.000    0.000    0.013    0.013 D:\Python27\lib\site-packages\PIL\Image.py:1943(open)
        1    0.010    0.010    0.010    0.010 {open}
        
------------------------------------------------------------------

IMAGE:                 9jan03-7.png

ALGORITHM OUTPUT:    [(True, 1.5693130963171611, -0.2151118303083011), (False, 2.019704984539922, -0.04808382089244378), (False, 1.9726509212744647, 0.23535764963143535)]

PROFILER OUTPUT:

Sat Jan 18 17:18:37 2014    profile_results

         759978 function calls (759977 primitive calls) in 3.915 seconds

   Ordered by: cumulative time
   List reduced from 130 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    3.915    3.915 <string>:1(<module>)
        1    0.000    0.000    3.915    3.915 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\AnalyseImage.py:16(test_case)
        1    0.000    0.000    3.915    3.915 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\AnalyseImage.py:11(analyse)
        1    0.000    0.000    3.915    3.915 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\Distance.py:12(__init__)
        1    1.000    1.000    3.462    3.462 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:51(startLumi)
        1    0.250    0.250    1.008    1.008 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:134(removeBackGround)
        1    0.758    0.758    0.758    0.758 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:296(onlyWhite)
        1    0.709    0.709    0.709    0.709 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:81(calculateGoalposts)
        1    0.349    0.349    0.408    0.408 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:24(getAverageLightIntensity)
    76800    0.314    0.000    0.362    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ColorSysCustom.py:43(rgb_to_hue)
   107520    0.137    0.000    0.192    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ColorSysCustom.py:7(rgb_to_luminance)
    76800    0.192    0.000    0.192    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:304(acceptedLumi)
   184320    0.061    0.000    0.061    0.000 {max}
   184326    0.042    0.000    0.042    0.000 {min}
    66669    0.029    0.000    0.029    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:318(acceptedYellow)
    62331    0.027    0.000    0.027    0.000 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:311(acceptedGreen)
        1    0.000    0.000    0.026    0.026 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\ImageProcessing.py:10(__init__)
        1    0.000    0.000    0.021    0.021 D:\Python27\lib\site-packages\PIL\Image.py:1943(open)
        1    0.001    0.001    0.019    0.019 D:\NAO-ALPHA-AS-FUCK-ROBOTS\Nao Robots\ImageProcessing\Distance.py:28(findLandmarks)
        1    0.017    0.017    0.017    0.017 {open}
        
------------------------------------------------------------------
'''