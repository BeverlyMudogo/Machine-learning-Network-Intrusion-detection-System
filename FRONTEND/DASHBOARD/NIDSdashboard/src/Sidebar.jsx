import React from 'react'
import { Link } from "react-router-dom" // Import Link for routing
import { GiPadlock } from "react-icons/gi" //  padlock icon
import { TbLayoutDashboard } from "react-icons/tb" // dashboard icon
import { MdNetworkCheck } from "react-icons/md" // network check (packet capture engine) icon
import { MdOutlineOnlinePrediction } from "react-icons/md" // pred icon
import {BsFillBellFill} from "react-icons/bs" // alerts
import { MdSettings } from "react-icons/md" // settings

function Sidebar({openSidebarToggle, OpenSidebar}){
    return (
        <aside id="sidebar" className={openSidebarToggle ? "sidebar-responsive": ""}>

            <div className='sidebar-title'>
                <div className='sidebar-brand'>
                    <GiPadlock className='icon_header'/> ML-NIDS
                </div>
                <span className='icon close_icon' onClick={OpenSidebar} >X</span>
            </div>

            <ul className='sidebar-list'>
                <li className='sidebar-list-item'>
                    <Link to='/'>
                        <TbLayoutDashboard className='icon' /> Dashboard
                    </Link>
                </li>
                <li className='sidebar-list-item'>
                    <Link to='/packet-capture'>{/*Packet capture route*/}
                        <MdNetworkCheck className='icon'/> Packet capture
                    </Link>
                </li>
                <li className='sidebar-list-item'>
                    <Link to='/predictions'>
                        <MdOutlineOnlinePrediction className='icon'/> Predictions
                    </Link>
                </li>
                <li className='sidebar-list-item'>
                    <a href="">
                        <BsFillBellFill className='icon'/> Alerts
                    </a>
                </li>
                <li  className='sidebar-list-item'>
                    <a href="">
                        <MdSettings className='icon' /> Settings
                    </a>
                </li>
            </ul>
        </aside>
    )
}

export default Sidebar