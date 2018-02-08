import Businesses from 'views/Businesses/Businesses';
import UserProfile from 'views/UserProfile/UserProfile';
import Login from 'views/Login/Login';
import AddBusiness from 'views/AddBusiness/AddBusiness';
import Register from 'views/Register/Register';
import Business from 'views/Business/Business';

const appRoutes = [
    { path: "/user", name: "User Profile", icon: "pe-7s-user", component: UserProfile },
    { path: "/Businesses", name: "Table List", icon: "pe-7s-note2", component: Businesses },
    { path: "/login", name: "User Login", icon: "pe-7s-user", component: Login },
    { path: "/addBusiness", name: "Items", icon: "pe-7s-user", component: AddBusiness },
    { path: "/Business", name: "Items", icon: "pe-7s-user", component: Business },
    { path: "/register", name: "Register", icon: "pe-7s-user", component: Register},
    { redirect: true, path: "/", to: "/login", name: "User Login" }
];

export default appRoutes;