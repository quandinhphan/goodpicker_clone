import React from 'react'
import { BrowserRouter, Switch, Route } from 'react-router-dom'
import UserProfilePage from './pages/user'
import HomePage from './pages/home'
import LoginPage from './pages/login'
import AboutUs from './pages/about-us'
import NewPost from './pages/new-post'
import Custom404 from './pages/404'
import { useAuthState, useAuthenticate, useLogout } from './hooks/useAuth'
import AuthService from './service/AuthService'

function App() {
	const { user, cookies } = useAuthState()
	const authenicate = useAuthenticate()
	const logout = useLogout()

	React.useLayoutEffect(() => {
		if (cookies['gp_token'] && !user) {
			AuthService.getMe(cookies['gp_token'])
				.then(res =>
					authenicate({ user: res.data, token: cookies['gp_token'] })
				)
				.catch(err => logout())
		}
	}, [cookies, user, authenicate, logout])

	return (
		<BrowserRouter>
			<div className="App">
				<div className="content">
					<Switch>
						<Route exact path="/" component={HomePage} />
						<Route exact path="/login" component={LoginPage} />
						<Route exact path="/profile" component={UserProfilePage} />
						<Route exact path="/about-us" component={AboutUs} />
						<Route exact path="/new-post" component={NewPost} />
						<Route component={Custom404} />
					</Switch>
				</div>
			</div>
		</BrowserRouter>
	)
}

export default App
