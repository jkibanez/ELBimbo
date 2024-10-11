import boto3
 
def copy_volume_tags(volume_id_1, volume_id_2):
    ec2 = boto3.client('ec2')
 
    # Get tags of the first volume
    response = ec2.describe_volumes(VolumeIds=[volume_id_1])
    tags = response['Volumes'][0].get('Tags', [])
 
    # Prepare tags for the second volume
    if tags:
        ec2.create_tags(Resources=[volume_id_2], Tags=tags)
        print(f"Copied tags from volume {volume_id_1} to volume {volume_id_2}.")
    else:
        print(f"No tags found for volume {volume_id_1}.")
 
# Example usage
copy_volume_tags('vol-0e956741048ed86d3', 'vol-0dc94532f91cd48fb')