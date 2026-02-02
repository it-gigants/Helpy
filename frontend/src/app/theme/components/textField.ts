import type { Components } from '@mui/material/styles';

export const textField: Components['MuiTextField'] = {
    variants: [
        {
            props: { variant: 'outlined' },
            style: {
                '& .MuiOutlinedInput-root': {
                    borderRadius: 8,
                },
            },
        },

        {
            props: { variant: 'standard' },
            style: {
                '& .MuiInput-underline:before': {
                    borderBottom: 'none',
                },
            },
        },

        {
            props: { error: true },
            style: {
                '& .MuiOutlinedInput-root': {
                    borderColor: '#f44336',
                },
            },
        },

        {
            props: { disabled: true },
            style: {
                opacity: 0.5,
            },
        },
    ],
};
