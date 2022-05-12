import {Checkbox, IconButton, ListItem, ListItemButton, ListItemIcon, ListItemText} from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete';

const Todo = (props) => {
    const todo = props.todo;
    const handleCheckChange = props.handleCheckChange;
    const del = props.delete;
    return(
    <ListItem key={props.id} secondaryAction={
        <IconButton aria-label="delete" onClick={(e) => del(todo.id)}>
            <DeleteIcon />
        </IconButton>} disablePadding>
         <ListItemButton onClick={(e) => handleCheckChange(props.id)}>
            <ListItemIcon>
                <Checkbox  checked={todo.is_complete === 1 ? true:false} />
            </ListItemIcon>
            <ListItemText primary={todo.text} />
         </ListItemButton>
    </ListItem>
    );
}
export default Todo;