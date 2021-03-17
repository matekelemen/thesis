# --- External Imports ---
import numpy

# --- STL Imports ---
import json


if __name__ == "__main__":
    JSONContents = json.loads("""
    {
        "domain" : 
            {
                "lengths" : [
                    0.5,
                    0.02,
                    0.01
                ],
                "rotationAngle" : 0.0,
                "meshScale" : [
                    1.00,
                    1.00,
                    1.0
                ],
                "time" : [
                    0.0,
                    0.5
                ]
            },
        "discretization" :
            {
                "numberOfElements" : [
                    100,
                    2,
                    1
                ],
                "deltaT" : 2e-4
            },
        "material":
            {
                "poissonRatio" : 0.0,
                "density" : 1e0,
                "youngsModulus" : 1e0
            },
        "model" :
            {
                "numberOfSolutionFields" : 1,
                "ansatzOrder" : 1,
                "integrationOrder" : 3,
                "partitioningDepth" : 2,
                "alphaFCM" : 1e-5,
                "lumpingScheme" : "none",
                "basisFunctions" : "fem",
                "forceImplicitTimeIntegration" : false
            },
        "load" :
            {
                "sourceMagnitude" : 1e0,
                "sourceFrequency" : 1e1,
                "numberOfCycles" : 1.0
            },
        "postprocessing" :
            {
                "postprocessingFrequency" : 50
            },
        "results": {
            "samplePoints": {
                "samplePoint0": [
                    "0.16666666666666666",
                    "0.01",
                    "0.0050000000000000001"
                ],
                "samplePoint1": [
                    "0.33333333333333331",
                    "0.01",
                    "0.0050000000000000001"
                ]
            }
        }
    }
    """)

    magnitudeMajor = 1.0
    magnitudeMinor = magnitudeMajor / 25
    period = 1.0 / float(JSONContents["load"]["sourceFrequency"])
    sourceFrequency =  2.0 * numpy.pi / period
    tMax = 2.0
    t0 = 2*period

    time = numpy.arange( start=0.0, stop=tMax, step=float(JSONContents["discretization"]["deltaT"]) )
    displacement = numpy.zeros( len(time) )

    for i, t in enumerate(time):
        if t0 <= t:
            if t <= t0 + period / 2.0:
                displacement[i] = magnitudeMajor * numpy.sin( sourceFrequency * (t-t0) )
            else:
                t = t - t0
                displacement[i] = magnitudeMinor * numpy.exp(-t) * numpy.sin( sourceFrequency * t )
        else:
            displacement[i] = magnitudeMinor * numpy.exp(t0-t) * numpy.sin( sourceFrequency * t )

    time = list(time)
    displacement = list(displacement)
    JSONContents["results"]["time"] = time
    JSONContents["results"]["samplePoint0"] = displacement
    JSONContents["results"]["samplePoint1"] = displacement

    with open( "generate_data_for_envelope_centroid.json", "w" ) as file:
        file.write( json.dumps(JSONContents, indent="    ") )