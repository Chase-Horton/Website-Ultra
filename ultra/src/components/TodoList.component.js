import Todo from './Todo.component'
const TodoList = (props) => {
    const todos = props.todos;
    const display = props.display;
    if(display == 'all'){
        return(
            <ul>
                {todos.map(todo => {
                    return(
                        <Todo key={todo.id} todo={todo} id={todo.id} handleCheckChange={props.handleCheckChange} delete={props.delete}/>
                    )
                })}
            </ul>
        );
    }
    else if(display == 'complete'){
        return(
            <ul>
                {todos.map(todo => {
                    if(todo.is_complete === 1){
                        return(
                            <Todo key={todo.id} todo={todo} id={todo.id} handleCheckChange={props.handleCheckChange} delete={props.delete}/>
                        );
                    }
                })}
            </ul>
        );
    }
    else if(display == 'incomplete'){
        return(
            <ul>
                {todos.map(todo => {
                    if(todo.is_complete === 0){
                        return(
                            <Todo key={todo.id} todo={todo} id={todo.id} handleCheckChange={props.handleCheckChange}/>
                        );
                    }
                })}
            </ul>
        );
    }
}
export default TodoList;