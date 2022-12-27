# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is all-in-one launch script intended for use by nav2 developers."""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition

from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Create the launch configuration variables
    namespace = LaunchConfiguration('namespace')
    port = LaunchConfiguration('port')
    address = LaunchConfiguration('address')
    ssl = LaunchConfiguration('ssl')
    certfile = LaunchConfiguration('certfile')
    keyfile = LaunchConfiguration('keyfile')
    retry_startup_delay = LaunchConfiguration('retry_startup_delay')
    fragment_timeout = LaunchConfiguration('fragment_timeout')
    delay_between_messages = LaunchConfiguration('delay_between_messages')
    max_message_size = LaunchConfiguration('max_message_size')
    unregister_timeout = LaunchConfiguration('unregister_timeout')

    # Launch configuration variables specific to simulation
    use_compression = LaunchConfiguration('use_compression')
    topics_glob = LaunchConfiguration('topics_glob')
    services_glob = LaunchConfiguration('services_glob')
    params_glob = LaunchConfiguration('params_glob')
    bson_only_mode = LaunchConfiguration('bson_only_mode')
    binary_encoder = LaunchConfiguration('binary_encoder')


    # Declare the launch arguments
    declare_namespace_cmd = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Top-level namespace')

    declare_port_cmd = DeclareLaunchArgument(
        'port',
        default_value= '9090',
        description='port number for socket connection')

    declare_address_cmd = DeclareLaunchArgument(
        'address',
        default_value='',
        description='ip address for connection')

    declare_ssl_cmd = DeclareLaunchArgument(
        'ssl',
        default_value='False',
        description='Whether to use ssl')

    declare_certfile_cmd = DeclareLaunchArgument(
        'certfile',
        default_value='',
        description='Full path to certfile')

    declare_keyfile_cmd = DeclareLaunchArgument(
        'keyfile',
        default_value='',
        description='full path to keyfile')

    declare_retry_startup_delay_cmd = DeclareLaunchArgument(
        'retry_startup_delay',
        default_value= '5.0',
        description= "")

    declare_fragment_timeout_cmd = DeclareLaunchArgument(
        'fragment_timeout', default_value= '600',
        description='')

    declare_delay_between_messages_cmd = DeclareLaunchArgument(
        'delay_between_messages', default_value= '0',
        description='')

    declare_max_message_size_cmd = DeclareLaunchArgument(
        'max_message_size', default_value= '10000000',
        description='')

    declare_unregister_timeout_cmd = DeclareLaunchArgument(
        'unregister_timeout',
        default_value='10.0',
        description='')

    declare_use_compression_cmd = DeclareLaunchArgument(
        'use_compression',
        default_value='False',
        description='')

    declare_topics_glob_cmd = DeclareLaunchArgument(
        'topics_glob',
        default_value='',
        description='')

    declare_services_glob_cmd = DeclareLaunchArgument(
        'services_glob',
        default_value='',
        description='')

    declare_params_glob_cmd = DeclareLaunchArgument(
        'params_glob',
        default_value='',
        description='')

    declare_bson_only_mode_cmd = DeclareLaunchArgument(
        'bson_only_mode',
        default_value='False',
        description='')

    declare_binary_encoder_cmd = DeclareLaunchArgument(
        'binary_encoder',
        default_value='default',
        description='')

    # Specify the actions
    start_rosbride_websocket_ssl_cmd = Node(
        condition=IfCondition(ssl),
        package='rosbridge_server',
        executable='rosbridge_websocket',
        name='rosbridge_websocket',
        namespace=namespace,
        output='screen',
        parameters=[{'port': port,
                     'address': address,
                     'certfile': certfile,
                     'keyfile': keyfile,
                     'retry_startup_delay': retry_startup_delay,
                     'fragment_timeout': fragment_timeout,
                     'delay_between_messages': delay_between_messages,
                     'max_message_size': max_message_size,
                     'unregister_timeout': unregister_timeout,
                     'use_compression': use_compression,
                     'topics_glob': topics_glob,
                     'serices_glob': services_glob,
                     'params_glob': params_glob}])
    
    start_rosbride_websocket_cmd = Node(
        condition=UnlessCondition(ssl),
        package='rosbridge_server',
        executable='rosbridge_websocket',
        name='rosbridge_websocket',
        namespace=namespace,
        output='screen',
        parameters=[{'port': port,
                     'address': address,
                     'retry_startup_delay': retry_startup_delay,                     
                     'fragment_timeout': fragment_timeout,
                     'delay_between_messages': delay_between_messages,
                     'max_message_size': max_message_size,
                     'unregister_timeout': unregister_timeout,
                     'use_compression': use_compression,
                     'topics_glob': topics_glob,
                     'serices_glob': services_glob,
                     'params_glob': params_glob}])

    start_rosapi_cmd = Node(
        package='rosapi',
        executable='rosapi_node',
        name='rosapi',
        namespace=namespace,
        output='screen',
        parameters=[{'topics_glob': topics_glob,
                     'serices_glob': services_glob,
                     'params_glob': params_glob}])

    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_namespace_cmd)
    ld.add_action(declare_port_cmd)
    ld.add_action(declare_address_cmd)
    ld.add_action(declare_ssl_cmd)
    ld.add_action(declare_certfile_cmd)
    ld.add_action(declare_keyfile_cmd)
    ld.add_action(declare_retry_startup_delay_cmd)
    ld.add_action(declare_fragment_timeout_cmd)
    ld.add_action(declare_delay_between_messages_cmd)
    ld.add_action(declare_max_message_size_cmd)
    ld.add_action(declare_unregister_timeout_cmd)
    ld.add_action(declare_use_compression_cmd)
    ld.add_action(declare_topics_glob_cmd)
    ld.add_action(declare_services_glob_cmd)
    ld.add_action(declare_params_glob_cmd)
    ld.add_action(declare_bson_only_mode_cmd)
    ld.add_action(declare_binary_encoder_cmd)

    

    # Add any conditioned actions
    ld.add_action(start_rosapi_cmd)
    ld.add_action(start_rosbride_websocket_ssl_cmd)
    ld.add_action(start_rosbride_websocket_cmd)

    return ld