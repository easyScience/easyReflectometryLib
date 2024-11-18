HTML_TEMPLATE = """<!DOCTYPE html>

<html>

    <style>
        th, td {
            padding-right: 18px;
        }
        th {
            text-align: left;
        }
    </style>

    <body>
        <table>
            <!-- Summary title -->
            <tr>
                <td><h1>Summary</h1></td>
            </tr>

            <!-- Project -->
            project_information_section
            
            <!-- Sample -->
            <tr>
                <td><h3>Sample</h3></td>
            </tr>
            sample_section

            <!-- Experiments -->
            <tr>
                <td><h3>Experiments</h3></td>
            </tr>
            experiments_section

            <!-- Analysis -->
            <tr>
                <td><h3>Refinement</h3></td>
            </tr>
            refinement_section

        </table>
    </body>
</html>"""


HTML_PROJECT_INFORMATION_TEMPLATE = """
<tr>
    <td><h3>Project information</h3></td>
</tr>

<tr>
    <th>Title</th>
    <th>project_title</th>
</tr>
<tr>
    <td>Description</td>
    <td>project_description</td>
</tr>
<tr>
    <td>No. of experiments</td>
    <td>num_experiments</td>
</tr>
"""

HTML_PARAMETER_HEADER_TEMPLATE = """
<tr>
    <th>parameter_name</th> 
    <th>parameter_value</th>
    <th>parameter_unit</th> 
    <th>parameter_error</th>
</tr>
"""

HTML_PARAMETER_TEMPLATE = """
<tr>
    <td>parameter_name</td> 
    <td>parameter_value</td>
    <td>parameter_unit</td> 
    <td>parameter_error</td>
</tr>
"""

HTML_DATA_COLLECTION_TEMPLATE = """
<tr>
    <th>Experiment datablock</th>
    <th>experiment_name</th>
</tr>
<tr>
    <td>Radiation probe</td>
    <td>radiation_probe</td>
</tr>
<tr>
    <td>Radiation type</td>
    <td>radiation_type</td>
</tr>
<tr>
    <td>Measured range: min, max, inc (range_units)</td>
    <td>range_min,&nbsp;&nbsp;range_max,&nbsp;&nbsp;range_inc</td>
</tr>
<tr>
    <td>No. of data points</td>
    <td>num_data_points</td>
</tr>
"""

HTML_REFINEMENT_TEMPLATE = """
<tr>
    <td>Calculation engine</td>
    <td>calculation_engine</td>
</tr>
<tr>
    <td>Minimization engine</td>
    <td>minimization_engine</td>
</tr>
<tr>
    <td>Goodness-of-fit: reduced <i>&chi;</i><sup>2</sup></td>
    <td>goodness_of_fit</td>
</tr>
<tr>
    <td>No. of parameters: total, free, fixed</td>
    <td>num_total_params, num_free_params, num_fixed_params</td>
</tr>
<tr>
    <td>No. of constraints</td>
    <td>num_constriants</td>
</tr>
"""
