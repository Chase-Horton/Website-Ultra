const Account = (props) => {
    const app = props.app;
    const account = app.state.account;
    return (
        <div>
            <h1>Account</h1>
            <p>id: {account.id}</p>
            <p>Username: {account.username}</p>
            <p>created: {account.account_creation.split('T')[0]}</p>
        </div>
    )
}
export default Account;