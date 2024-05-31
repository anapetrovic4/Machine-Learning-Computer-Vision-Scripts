
# PDAL Pipeline Example Usage
This README provides an example usage of a PDAL (Point Data Abstraction Library) pipeline to downsample a LAS file. The pipeline reads a LAS file, applies voxel downsampling, and writes the downsampled point cloud to a new LAS file.

## Requirements

* PDAL installed on your system
* Input LAS file available at the specified path

## Pipeline JSON Structure

The following JSON structure defines the PDAL pipeline:

```
{
    "pipeline": [
        {
            "type": "readers.las",
            "filename": "AP_Merge_Las_Files/Blok 2.las"
        }, 
        {
            "type": "filters.voxeldownsize",
            "cell": 0.5,
            "mode": "center"
        },
        {
            "type": "writers.las",
            "filename": "AP_Merge_Las_Files/Blok 2 downsampled.las"
        }
    ]
}
```

## Pipeline Components
1. **readers.las**: This component reads the input LAS file.

   * **type**: Specifies the reader type. Here, it is **readers.las**.
   * **filename**: Path to the input LAS file.

2. **filters.voxeldownsize**: This component performs voxel downsampling on the point cloud data.

   * **type**: Specifies the filter type. Here, it is **filters.voxeldownsize**.
   * **cell**: Specifies the size of the voxel grid cell. A smaller value retains more detail.
   * **mode**: Specifies the downsampling mode. **center** uses the center of the voxel grid cell.

3. **writers.las**: This component writes the downsampled point cloud to a new LAS file.

   * **type**: Specifies the writer type. Here, it is **writers.las**.
   * **filename**: Path to the output LAS file.

## Running the Pipeline

To run the PDAL pipeline, follow these steps:

   1. Save the pipeline JSON structure to a file, for example, **downsample_pipeline.json**.

   2. Execute the PDAL pipeline using the following command:

`pdal pipeline downsample_pipeline.json`
