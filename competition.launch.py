from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    
    node1_selector = Node(
        package='mia_competition',
        executable='select_node',
        name='cmd_multiplexer',
        output='screen'
    )

  
    node2_auto = Node(
        package='mia_competition',
        executable='auto_node',
        name='autonomous_controller',
        output='screen'
    )

    
    node3_manual = Node(
        package='mia_competition',
        executable='manual_node',
        name='pilot_teleop',
        output='screen',
        prefix=['gnome-terminal --']
    )

    return LaunchDescription([
        node1_selector,
        node2_auto,
        node3_manual
    ])